# -*- coding: utf-8 -*-
"""
    fortigate_vpn_login.cli
    ~~~~~~~~~~~~~~~~~~~~~~

    This is the CLI interface for running the package.
"""
import logging
import os
import sys
import webbrowser
import subprocess
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from fortigate_vpn_login import __version__, __description__, logger
from fortigate_vpn_login import utils, config
from fortigate_vpn_login.fortigate import Fortigate
import fortigate_vpn_login.webserver as webserver


def main() -> int:
    """
    Main method which is called by CLI.

    Returns:
        int: The status from the program.

    Exit codes:
        0: Everything went well.
        1: General error while connecting to the VPN
        2: Usage/syntax error
    """
    # main program argument parser
    parser = ArgumentParser(
        formatter_class=RawDescriptionHelpFormatter,
        description=(
            f"fortigate-vpn-login {__version__}{os.linesep}"
            f"{__description__}"
        )
    )

    parser.add_argument(
        '-d',
        '--debug',
        help='Set LOG_LEVEL to DEBUG.',
        dest="DEBUG_MODE",
        action='store_true'
    )

    parser.add_argument(
        '-q',
        '--quiet',
        help='Do not log at all.',
        dest="QUIET_MODE",
        action='store_true'
    )

    parser.add_argument(
        '--configure',
        help='Interactive configuration.',
        dest='INTERACTIVE_CONFIGURE',
        action='store_true'
    )

    parser.add_argument(
        '-s',
        '--forti-url',
        help='URL of the Fortigate VPN server.',
        dest='FORTI_URL'
    )

    # windows don't have these options supported
    if not utils.is_windows():
        parser.add_argument(
            '-F',
            '--foreground',
            help='Run VPN in foreground.',
            dest="FOREGROUND",
            action='store_true'
        )

        parser.add_argument(
            '-B',
            '--background',
            help='Run VPN in background (default).',
            dest="BACKGROUND",
            action='store_true',
            default=True
        )

    # parse the arguments, show in the screen if needed, etc
    parser = parser.parse_args()

    if parser.DEBUG_MODE:
        logger.setLevel("DEBUG")
        logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "DEBUG"))
        # TODO: on debug mode, change log format to
        # '[%(asctime)s] [%(levelname)s] [%(name)s:%(filename)s:%(lineno)s: %(funcName)s()] %(message)s'))
    else:
        # defaults to info
        logger.setLevel("INFO")
        logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "INFO"))

    if parser.QUIET_MODE:
        logging.disable(logging.CRITICAL)

    if parser.FOREGROUND:
        parser.BACKGROUND = False

    # load configuration
    options = config.Config()

    # do we need to configure interactively?
    if parser.INTERACTIVE_CONFIGURE:
        options.configure()
        options.write()
        return 0

    openconnect_path = utils.find_openconnect()

    # openconnect compatability check
    if not utils.check_openconnect_version(openconnect_path):
        print("ERROR: Your openconnect version isn't compatible with this program. "
              "Make sure you have the latest version, which supports the \"fortinet\" protocol.")
        return 1

    # server url
    if not parser.FORTI_URL:
        fortigate_vpn_url = options.get('forti_url')
        if not fortigate_vpn_url:
            print('ERROR: "forti_url" option is not set. Use "-s" or "--configure" to set it.')
            return 2
    else:
        fortigate_vpn_url = parser.FORTI_URL

    # establish connection to the Fortigate VPN Server, grab info, etc
    fortigate = Fortigate(fortigate_vpn_url)
    url = fortigate.connect_saml()
    if not url:
        return 1

    # webserver to get the response from the IDP through browser request
    ws = webserver.run()
    webbrowser.open(url)
    auth_id = webserver.return_token()
    webserver.quit(ws)

    if auth_id == '-1':
        print("ERROR: Invalid ID from provider. Try again or contact your provider support.")
        return 1

    cookie_svpn = fortigate.get_cookie(auth_id)

    openconnect_arguments = [
        "--protocol=fortinet",
        f"--server={fortigate_vpn_url}",
        f"--useragent=fortigate-vpn-login-{__version__}:{os.uname().version}",
        "--no-dtls",
        "--non-inter",
        "--disable-ipv6",
        f"--cookie=SVPNCOOKIE={cookie_svpn}",
    ]

    if parser.QUIET_MODE:
        openconnect_arguments.append("--quiet")

    if parser.DEBUG_MODE:
        openconnect_arguments.append("--verbose")

    if parser.BACKGROUND:
        openconnect_arguments.append("--quiet")
        openconnect_arguments.append("--background")

    command_line = []
    if utils.is_windows():
        workdir = openconnect_path.parent
        command_line = [
            "powershell",
            "-Command",
            f"Start-Process '{str(openconnect_path)}' "
            f"-ArgumentList {','.join(openconnect_arguments)} "
            f"-Verb runAs -WorkingDirectory {workdir}",
        ]
    else:
        if not os.getuid() == 0:
            command_line.append("sudo")
            command_line = command_line + [str(openconnect_path)] + openconnect_arguments

    env = os.environ.copy()
    env['LC_ALL'] = 'C'

    try:
        if not parser.BACKGROUND:
            subprocess.run(command_line, env=env)
        else:
            subprocess.run(command_line, env=env,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except KeyboardInterrupt:
        logger.debug("User interrupted process.")
        print("CTRL+C/SIGTERM detected. Exiting.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
