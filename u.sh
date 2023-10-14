git fetch
git pull
systemctl restart tktpyp
systemctl status tktpyp
sudo journalctl --rotate
sudo journalctl --vacuum-time=1s