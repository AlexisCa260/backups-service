import socket

import paramiko

from config import SSH_PASS, SSH_TIMEOUT, SSH_USER


def obtener_configuracion_ssh(ip: str) -> str:
    client = None
    intentos_algoritmos = [
        {},
        {
            "kex": [
                "diffie-hellman-group-exchange-sha1",
                "diffie-hellman-group14-sha1",
            ],
            "cipher": ["aes128-cbc", "3des-cbc"],
        },
    ]

    for intento, disabled in enumerate(intentos_algoritmos, start=1):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                ip,
                username=SSH_USER,
                password=SSH_PASS,
                look_for_keys=False,
                allow_agent=False,
                timeout=SSH_TIMEOUT,
                banner_timeout=SSH_TIMEOUT,
                auth_timeout=SSH_TIMEOUT,
                disabled_algorithms=disabled or None,
            )

            stdin, stdout, stderr = client.exec_command("show running-config")
            output = stdout.read().decode(errors="ignore").strip()
            client.close()
            return output if output else "SSH conectado pero sin salida del comando."

        except paramiko.ssh_exception.SSHException as e:
            msg = str(e)
            if ("No existing session" in msg or "handshake" in msg) and intento < len(
                intentos_algoritmos
            ):
                continue
            return f"Error SSH ({ip}): {msg}"

        except paramiko.ssh_exception.NoValidConnectionsError:
            return f"Error SSH ({ip}): TCP connection to device failed."

        except socket.timeout:
            return f"Error SSH ({ip}): Timeout ({SSH_TIMEOUT}s)."

        except Exception as e:
            return f"Error SSH ({ip}): {str(e)}"

        finally:
            if client:
                client.close()

    return f"Error SSH ({ip}): Fallaron todos los intentos."
