from task import Runner

become_user_password = 'foo-whatever'
run_data = {
    'user_id': 12345,
    'foo': 'bar',
    'baz': 'cux-or-whatever-this-one-is'
}

runner = Runner(
    hostnames='192.168.10.233',
    playbook='run.yaml',
    private_key='/home/user/.ssh/id_whatever',
    run_data=run_data,
    become_pass=become_user_password,
    verbosity=0
)

stats = runner.run()

# Maybe do something with stats here? If you want!
print stats