source UPPMAX\ 2021_1-5-openrc-3.sh
python ssc-instance-userdata.py
echo ""
echo "<----- now wait for vm to contexualize, around 10m ----->"
echo ""
echo "Meanwhile look at the following output in order to use the application just deployed "
echo ""
openstack server show C3_task1 -f json
echo ""
echo "Description of above output:"
echo ""		
echo "UPPMAX 2021/1-5 Internal IPv4 Network: [
      <Private IP>,
      <Floating IP>  <-----------   This is the floating IP"
echo ""
echo "Run the followng command in the terminal with floating IP presented above: $ curl -i http://<Floating IP>:5000/start_count"
echo ""
echo "Or enter the following in your web browser: http://<Floating IP>:5000/start_count"

