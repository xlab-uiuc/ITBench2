# IT Automation Testbed for Open Source 

## Setup

### Local Cluster

For instruction on how to create a KIND cluster, please see the instructions [here](./local_cluster/README.md).

### Remote Cluster

For instruction on how to create an cloud provider based Kubernetes cluster, please see the instructions [here](./remote_cluster/README.md). 

Currently, only AWS is supported.

## Hacking

1. Create the `all.yaml` file from the template and update the `kubeconfig` field with the path to the configuration of the Kubernetes cluster. While the file creation needs only to be done once, the `kubeconfig` field must be updated if the file path changes.

```bash
cp group_vars/all.yaml.example group_vars/all.yaml
```

2. Deploy the observability tools. To remove the tools, run the `undeploy` version of the following `make` command.

```bash
make deploy_observability_stack
```

3. Deploy the sample application. To remove the application, run the `undeploy` version of the following `make` command.

```bash
make deploy_astronomy_shop
```

or 

```bash
make deploy_hotel_reservation
```

4. Once all pods are running, inject the fault for an incident.

```bash
INCIDENT_NUMBER=1 make inject_incident_fault
```

5. To remove the injected fault, run the following `make` command:

```bash
INCIDENT_NUMBER=1 make remove_incident_fault
```

_Note_: For a full list of `make` commands, run the following command:

```bash
make help
```

## Contributing

To contribute an incident to the testbed, follow these steps:

1. Create an incident directory.

```bash
mkdir roles/incident_<number>
mkdir roles/incident_<number>/tasks
touch roles/incident_<number>/tasks/main.yaml
mkdir roles/incident_<number>/vars
touch roles/incident_<number>/vars/main.yaml
```

2. Add the following variables to the `vars/main.yaml` file of the new incident. Modify the values of each field as needed. The current available domains are `sre` and `finops`. The current available sample applications are `otel_astronomy_shop` and `dsb_hotel_reservation`.

```yaml
scenario_domain: sre
sample_application: dsb_hotel_reservation
```

3. Add any more variables needed for the execution of the tasks.

4. Add the tasks to the `tasks/main.yaml` file. All tasks should have the tag `incident_<number>`, where `<number>` is the number of the new incident. Tasks needed for the fault inject should only run when the variable `is_fault_injection` is true. Tasks needed for fault removal should only run when the variable `is_fault_removal` is true. See the existing tasks for details.

5. Add documentation. See the existing tasks for details. Upon completion, run the following command:

```bash
make documentation
```

_Note_: To contribute a FlagD-based (native) incident scenario please refer to the commit [here](https://github.ibm.com/DistributedCloudResearch/IT-Automation-Testbed/commit/338995e3943dedb08d3cbd2edb5acaa58a41ef50) for reference.

_Note_: To contribute a Chaos-Mesh-based incident scenario please refer to commit [here](https://github.ibm.com/DistributedCloudResearch/IT-Automation-Testbed/commit/981750fbc2c02b721330209333bc87fdab932afa) for reference.  
