import base64
import os
import sys

from karton2 import Config


def patch_config(cfg):
    cfg = Config(cfg)

    try:
        access_key = cfg.config['minio']['access_key']
        secret_key = cfg.config['minio']['secret_key']
    except KeyError:
        sys.stderr.write('WARNING! Misconfiguration: section [minio] of config.ini doesn\'t contain access_key or secret_key.')
        return cfg

    if not access_key and not secret_key:
        with open('/etc/drakcore/minio.env', 'r') as f:
            minio_cfg = [line.split('=', 1) for line in f if line.strip() and '=' in line]
            minio_cfg = {k: v for k, v in minio_cfg}

        try:
            cfg.config['minio']['access_key'] = minio_cfg['ACCESS_KEY']
            cfg.config['minio']['secret_key'] = minio_cfg['SECRET_KEY']
        except KeyError:
            sys.stderr.write('WARNING! Misconfiguration: minio.env doesn\'t contain ACCESS_KEY or SECRET_KEY.')

    return cfg
