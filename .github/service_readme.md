In order to run the GitHub action, we need to run the remote actions runner on the server.
Currently, we use Ubuntu 19.10.
After cloning the actions runner into the server, change the name of `run.sh` file to `ActionsRunner.sh` (this is so we can find the runner process by its name later).
Copy the 'ActionsRunner.service' script in this directory into /etc/systemd/system
Make sure to replace user= with your own username, and update the directory of the actions runner.
Verify that this worked by running `sudo systemctl start ActionsRunner`
You should see the runner and the listeners in the processes (e.g. with `htop` or `ps ax`).
Next, verify that we can shut down the actions runner with `sudo systemctl stop ActionsRunner`.

