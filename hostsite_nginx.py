import re
import os
import sys
import subprocess
from execUtils import exec_cmd, pip_install
import logging
logging.basicConfig(filename="hostsite_nginxunit.log", level=logging.INFO)


def delete_site(site_name="example", site_domain="in"):
    if os.path.exists(f"/var/www/htdocs/{site_name}{site_domain}"):
        exec_cmd(
            f"""doas rm -rf    /var/www/htdocs/{site_name}.{site_domain}  /etc/nginx/conf.d/{site_name}.{site_domain}.conf""".split()
        )


def add_unit_listener(site_name="example", site_domain="in", app_module="simpleapp", app_port=29000):

    os.chdir(f"""/var/www/htdocs/{site_name}.{site_domain}""")
    os.system("""doas sh /tmp/build_venv.sh""")
    os.system("""doas chown -R adming:www venv/""")

    unit_json = f"""
        {{
    "listeners": {{
        "127.0.0.1:{app_port}": {{
            "pass": "applications/fastapi"
        }}
    }},

    "applications": {{
        "fastapi": {{
            "type": "python 3.10",
            "path": "/var/www/htdocs/{site_name}.{site_domain}",
            "home": "/var/www/htdocs/{site_name}.{site_domain}/venv",
            "module": "{app_module}",
            "callable": "app"
        }}
    }}
    }}
    """

    with open(f"/tmp/{site_name}.unit_cfg", "w") as fh:
        fh.write(unit_json)

    print("config unit")
    os.system(f"""
    doas curl -X PUT --data-binary @/tmp/{site_name}.unit_cfg  --unix-socket /var/run/unit/control.sock http://localhost/config
    """)
    logging.info(f"""
    doas curl -X PUT --data-binary @/tmp/{site_name}.unit_cfg  --unix-socket /var/run/unit/control.sock http://localhost/config
    """)

    pass


def host_site(site_name="example", site_domain="in", port=80, app_module="simpleapp", app_port=29000):
    content_tgz_fn = f"{site_name}.{site_domain}.tgz"
    maintainer_email = os.environ['maintainer_email']

    try:
        res = exec_cmd(
            f"mkdir /tmp/{site_name}.{site_domain}".split())
        logging.info(res)

        os.chdir(f"/tmp/{site_name}.{site_domain}")
        res = exec_cmd(
            f"tar xvzf /tmp/{content_tgz_fn}".split())
        logging.info(res)

        # os.chdir(f"/var/www/htdocs/{site_name}{site_domain}")
        cmdl = f"""doas  mv /tmp/{site_name}.{site_domain}  /var/www/htdocs/ """.split(
        )
        exec_cmd(cmdl)
        logging.info(res)
        # ============================= done =============================
        if "ssl_certificate" not in open(f"/etc/nginx/conf.d/{site_name}.{site_domain}.conf").read():
            site_directive = f"""
            upstream {site_name}_app_endpoint {{
            server 127.0.0.1:{app_port};
            }}

            server {{
            listen         {port} default_server;
            listen         [::]:{port} default_server;
            server_name    {site_name}.{site_domain} www.{site_name}.{site_domain};
            root           /var/www/htdocs/{site_name}.{site_domain};
            location / {{
            proxy_pass http://{site_name}_app_endpoint;
            }}

    }}"""

            with open(f"/tmp/{site_name}.{site_domain}.conf", "w") as fh:
                fh.write(site_directive)

            cmdl = ["doas", "cp", f"/tmp/{site_name}.{site_domain}.conf",
                    "/etc/nginx/conf.d/"]
            exec_cmd(cmdl)
            logging.info(res)
            # os.system(
            #     """doas certbot --nginx -d www.{site_name}.{site_domain}  -m {maintainer_email} --agree-tos""")

            os.system("chmod +x  /tmp/run_certbot.sh")

            os.system(
                f"""doas sh /tmp/run_certbot.sh {site_name} {site_domain} {maintainer_email}""")

        add_unit_listener(site_name, site_domain, app_module, app_port)

    except Exception as e:
        raise e
    finally:
        res = exec_cmd(
            f"rm -f /tmp/{site_name}.{site_domain}".split())


def install():
    # sites := [['example', 'in'], ['terible', 'com']]
    sites = [_ for _ in map(lambda aline, tt=re.compile(
        "[ |.]"): tt.split(aline.strip()), open("sites.txt").readlines())]

    for dn, tld, port, app_module, app_port in sites:
        delete_site(dn, tld)
        host_site(dn, tld, port, app_module, app_port)
    # restart nginx


if os.path.exists("/tmp/env.sh"):
    install()
