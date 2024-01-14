param($PubKeyPath)

$create_vm_output = yc compute instance create --public-ip `
    --ssh-key $PubKeyPath `
    --create-boot-disk image-id=fd8narkhqt532c99enpq `
    --core-fraction 20;

$instance_id = ([regex]'id: (.*?) ').Matches($create_vm_output).Groups[1];
$instance_internal_ip = ([regex]' address: (.*?) ').Matches($create_vm_output)[0].Groups[1];
$instance_subnet_id = ([regex]' subnet_id: (.*?) ').Matches($create_vm_output)[0].Groups[1];

yc load-balancer target-group update `
    --id enpbetinst7moo3bqvkk `
    --target address=$instance_internal_ip,subnet-id=$instance_subnet_id