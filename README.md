# ACC_CA3

Download the repository, add your own Openstack RC File v3 in the Deploy folder, and also the key-pair that you say you will use in the **ssc-instance-userdata.py**. The **ssc-instance-userdata.py** has to be modified, change the following rows:   
keypair = _<key pair in your folder, example if key.pem enter just key>_  
instance-name =_<choose a name for your instance>_  

then do the following at the ACC_CA3/Deploy folder in the terminal:

```
./deploy-vm.sh
```
