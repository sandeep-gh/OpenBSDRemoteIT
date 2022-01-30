import importlib
import os
import subprocess
from manage_env import build_env, add_to_env
from deployConfig import workDir, logDir, scriptsDir


def exec_script(targetNode, scriptFn, dependsFiles=[], user="adming", execDir="/tmp", manageEnv=True, dependsPkgs=[],  logOutput=None):
    """
    copy the script to remote and run it
    """

    def exec_clush_cmd(cmdargl):
        """
        cmdargl: clush command argument as a list
        """
        print("cmd = ", cmdargl)
        res = subprocess.check_output(
            ["clush", "-l", user, "-w", targetNode,  *cmdargl])
        # in case you don't like the output
        # https://stackoverflow.com/questions/42965689/replacing-a-text-with-n-in-it-with-a-real-n-output
        #formatted_output = res.replace('\\n', '\n').replace('\\t', '\t')
        return res.decode("utf-8")

    def ship_to_remote(source_fp, target_dir="/tmp"):
        res = exec_clush_cmd(
            f"--copy {source_fp} --dest {target_dir}/".split())
        return res

    def ship_from_remote(source_fp, target_dir="/tmp"):
        res = exec_clush_cmd(
            f"--rcopy {source_fp} --dest {target_dir}/".split())
        return res

    if manageEnv:
        with open("/tmp/env.sh", "w") as fh:
            fh.write(build_env())

        res = ship_to_remote("/tmp/env.sh")
        res = exec_clush_cmd(
            "chmod +x /tmp/env.sh".split())

    if dependsPkgs:
        doas = "doas"
        if user == "root":
            doas = ""
        res = exec_clush_cmd(
            f"""{doas} pkg_add {" ".join(dependsPkgs)}""".split())

    dependsFiles = [*dependsFiles, "execUtils.py"]

    depends_clean_cmd = ""
    damps = ""
    if dependsFiles:
        for _ in dependsFiles:
            adir = os.path.dirname(_)
            print("debug ", _, "L ", adir)
            if adir == '':
                adir = workDir
            aname = os.path.basename(_)
            print("res= ", os.path.exists(
                f"{adir}/{aname}"), f"{adir}/{aname}")
            if not os.path.exists(f"{adir}/{aname}"):
                adir = scriptsDir
            ship_to_remote(f"{adir}/{aname}")
            # res = exec_clush_cmd(
            #     f"--copy {adir}/{aname} --dest /tmp".split())
            damps = "&&"
            depends_clean_cmd += f" {damps} rm /tmp/{aname}"

    adir = workDir
    if not os.path.exists(f"{adir}/{scriptFn}"):
        adir = scriptsDir
    res = ship_to_remote(f"{adir}/{scriptFn}")
    # res = exec_clush_cmd(
    #     f"--copy {adir}/{script_fn} --dest /tmp".split())

    load_env = ""
    if manageEnv:
        load_env = ". /tmp/env.sh;"
    print(depends_clean_cmd)
    depends_clean_cmd = ""
    res = exec_clush_cmd(f"""
                         cd {execDir} && 
{load_env}  python3 /tmp/{scriptFn}  {depends_clean_cmd}""".split())
    if manageEnv:
        os.remove("/tmp/env.sh")
    if logOutput:
        ship_from_remote(f"/tmp/{logOutput}", logDir)
