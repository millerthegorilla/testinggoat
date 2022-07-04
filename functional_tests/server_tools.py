from fabric.api import run
from fabric.context_managers import settings, shell_env


def _get_server_env_vars(host):
    env_lines = run('cat ~/src/obey_the_testing_goat/code/superlists/settings.py')
    return dict(l.split('=') for l in env_lines if '=' in l)

def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'dev@{host}'):
        env_vars = _get_server_env_vars(host)
        with shell_env(**env_vars):
            session_key = run(f'{manage_dot_py} create_session {email}')
            return session_key.strip()

def _get_manage_dot_py(host):
    return f'~/src/obey_the_testing_goat/bin/python ~/src/obey_the_testing_goat/code/manage.py'

def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'dev@{host}'):  
        run(f'{manage_dot_py} flush --noinput')  
