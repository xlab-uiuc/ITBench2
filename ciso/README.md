# CISO (Chief Information Security Officer) Sample Task Scenarios

This repository provides sample task scenarios of the IT Benchmark for CISO. Each scenario includes a setup for a compliance misconfigured environment and tools to check and address if the misconfiguration is resolved or not.

This repository contains following 4 category of scenarios:

```
.
├── 1.gen-cis-b-k8s-kyverno
├── 2.gen-cis-b-k8s-kubectl-opa
├── 3.gen-cis-b-rhel9-ansible-opa
├── 4.upd-cis-b-k8s-kyvernoz
└── README.md
```

## Scenarios

### 1. gen-cis-b-k8s-kyverno
**Description**: This scenario expects to deploy Kyverno policies to detect injected compliance issues in a Kubernetes environment for the compliance requirement "Minimize the admission of containers wishing to share the host network namespace".

1. The agent is expected to do following task request (template value will be substituted):

    ```
    I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`
    Minimize the admission of containers wishing to share the host network namespace

    To check the condition, do the following steps. 
    - deploy a Kyverno policy to the cluster
    - chcek if the policy is correctly deployed. 

    If deploying the policy failed and if you can fix the issue, you will do it and try deploying again.
    Once you get a final answer, you can quit the work.

    The cluster's kubeconfig is at `{{ kubeconfig }}`.
    ```

    When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)

    ```json
    {
        "metadata": {
            "name": "cis-b.5.2.5-gen",  // Scenario Name
            "description": "CIS Benchmark for K8S 5.2.5 (Kyverno)", // Scenario Description
            "scenario_type": "Gen-CIS-b-K8s-Kyverno" // Scenario Type
        },
        // The above goal description
        "goal_template": "I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`\n    Minimize the admission of containers wishing to share the host network namespace.\n\nTo check the condition, do the following steps. \n- deploy a Kyverno policy to the cluster\n- chcek if the policy is correctly deployed. \n\nIf deploying the policy failed and if you can fix the issue, you will do it and try deploying again.\nOnce you get a final answer, you can quit the work.\n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
        "vars": {
            "kubeconfig": "apiVersion: v1\ncluster...="  // kubeconfig.yaml contents for access to the target Kubernetes
        }
    }
    ```

1. How it is evaluated

    The evaluation verifies the following to return a pass:
    - Verify that the specified Kyverno policy produces the expected Kyverno policy report for the target resource.

    Please refer to [evaluation/main.py](/ciso/1.gen-cis-b-k8s-kyverno/evaluation/main.py) for the details.

**The contents of the directory**:
```
├── 1.k8s-kyverno
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Kyverno Policy to detect the compliance violation
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

### 2. gen-cis-b-k8s-kubectl-opa
**Description**: This scenario expects to use kubectl to collect the Kubernetes resources and OPA (Open Policy Agent) to check if the injected compliance issues are detected or not for the compliance requirement "Minimize the admission of containers wishing to share the host network namespace".

1. The agent is expected to do following task request (template value will be substituted):

    ```
    I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`
        Minimize the admission of containers wishing to share the host network namespace

    To check the condition, do the following steps. 
    - get related resource(s) on the cluster by kubectl command
    - chcek if the conditions are satisfied by OPA Rego policy

    for those steps, you need to create an OPA Rego policy `policy.rego`. 
    Also, save the kubectl command as `script.sh` with the following design. 
    - The script should output the collected related resources to a file named `collected_data.json` in the current working directory.
    - Please remove any kubeconfig configuration (e.g. --kubeconfig args) from the script, as users will configure the kubeconfig using environment variables or other methods.

    If running the policy failed and if you can fix the issue, you will do it and try running again.

    Once you get a final answer, you can quit the work.

    The cluster's kubeconfig is at `{{ kubeconfig }}`.
    ```

    When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)
    ```json
    {
        "metadata": {
            "name": "k8s-opa/cis-b-gen/5.2.5", // Scenario Name
            "description": "CIS Benchmark for K8S 5.2.5 (OPA)", // Scenario Description
            "scenario_type": "Gen-CIS-b-K8s-Kubectl-OPA" // Scenario Type
        },
        // The above goal description
        "goal_template": "I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`\n    Minimize the admission of containers wishing to share the host network namespace. \n\nTo check the condition, do the following steps. \n- get related resource(s) on the cluster by kubectl command\n- chcek if the conditions are satisfied by OPA Rego policy\n\nfor those steps, you need to create an OPA Rego policy `policy.rego`. \nAlso, save the kubectl command as `script.sh` with the following design. \n- The script should output the collected related resources to a file named `collected_data.json` in the current working directory.\n- Please remove any kubeconfig configuration (e.g. --kubeconfig args) from the script, as users will configure the kubeconfig using environment variables or other methods.\n\nIf running the policy failed and if you can fix the issue, you will do it and try running again.\n\nOnce you get a final answer, you can quit the work.\n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
        "vars": {
            "kubeconfig": "apiVersion: v1\nclusters:\n- ..." // kubeconfig.yaml contents for access to the target Kubernetes
        }
    }
    ```

1. How it is evaluated

    The evaluation verifies the following to return a pass:
    - Confirm that the script.sh and policy.rego are produced.
    - Ensure that script.sh runs successfuly and verify that the collected_data.json is produced.
    - Ensure that OPA command runs successfully with the policy.rego against the collected_data.json. 
    - Verify that the OPA outputs expected result.

    Please refer to [evaluate.yml](/2.gen-cis-b-k8s-kubectl-opa/playbooks/evaluate.yml) for the details.

**The contents of the directory**:
```
├── 2.k8s-kubectl-opa
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example scripts to fetch Kubernetes resources and OPA Rego policy to check if the statuses complies or not 
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

### 3. gen-cis-b-rhel9-ansible-opa
**Description**: This scenario expects to use Ansible Playbooks to collect system status from RHEL9 and OPA to check if the injected compliance issues are detected or not for the compliance requirement "Ensure SSH X11 forwarding is disabled".

1. The agent is expected to do following task request (template value will be substituted):

    ```
    I would like to check if the following condition is satisfiled, given a host name `rhel9_servers`, on RHEL by using Ansible Playbook and OPA Rego policy
        Ensure SSH X11 forwarding is disabled

    To check the condition, do the following steps. 
    - collect configuration from the RHEL host and save it locally. you can use ansible-playbook to do that. 
    - chcek if the condition is met by using rego policy with the input given by the step above. 

    for those steps, you need to create ansible playbook `playbook.yml` and OPA rego policy `policy.rego`.
    The playbook is implemented to locate the collected data to a file named `collected_data.json` in the current working directory.

    If you can fix the generated code, do it and run the fixed code again.
    Once you get a final answer, you can quit the work.

    The Ansible inventory file (inventory.ansible.ini) for the target RHEL server is located at `{{ path_to_inventory }}`.
    ```

    When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)
    ```json
    {
    "metadata": {
        "name": "rhel9/cis-b-gen/5.2.12", // Scenario Name
        "description": "CIS Benchmark for RHEL9 5.2.12", // Scenario Description
        "scenario_type": "Gen-CIS-b-RHEL9-Ansible-OPA" // Scenario Type
        },
        // The above goal description
        "goal_template": "I would like to check if the following condition is satisfiled, given a host name `rhel9_servers`, on RHEL by using Ansible Playbook and OPA Rego policy\n    Ensure SSH X11 forwarding is disabled \n\nTo check the condition, do the following steps. \n- collect configuration from the RHEL host and save it locally. you can use ansible-playbook to do that. \n- chcek if the condition is met by using rego policy with the input given by the step above. \n\nfor those steps, you need to create ansible playbook `playbook.yml` and OPA rego policy `policy.rego`.\nIf you can fix the generated code, do it and run the fixed code again.\nOnce you get a final answer, you can quit the work.\n\nThe Ansible inventory file (inventory.ansible.ini) for the target RHEL server is located at `{{ path_to_inventory }}`.\n",
        "vars": {
            "ansible_ini": "[rhel9_servers]\nrhel9 ansible_host=...", // Ansible Ini file to acceess to the target RHEL system
            "ansible_user_key": "***" // SSH Key
        }
    }
    ```

1. How it is evaluated

    The evaluation verifies the following to return a pass:
    - Confirm that the playbook.yml and policy.rego are produced.
    - Ensure that playbook.yml runs successfuly and verify that the collected_data.json is produced.
    - Ensure that OPA command runs successfully with the policy.rego against the collected_data.json. 
    - Verify that the OPA outputs expected result.
    
    Please refer to [evaluate.yml](/3.gen-cis-b-rhel9-ansible-opa/playbooks/evaluate.yml) for the details.

**The contents of the directory**:
```
├── 3.rhel9-ansible-opa
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Ansible Playbook to fetch system statuses and OPA Rego policy to check if the statuses complies or not 
│   └── Makefile    # Commands to simplify setup and execution for the scenario
│   └── tasks
│       ├── fault_inject.yml # Ansible task to make the RHEL system compliance violation
```

### 4. upd-cis-b-k8s-kyvernoz
**Description**: This scenario expects to inspect the current Kyvero policies and Kubernetes resources, then update the existing policies to comply the new compliance requirements.

1. The agent is expected to do following task request (template value will be substituted):

    ```
    Currently, the following Kyverno policies are deployed in the Kubernetes cluster. Review these existing policies and edit them to meet additional security requirements. Please avoid creating new policy resources; instead, make the necessary changes directly to the existing resources.

        Prohibit the use of the default service account
        Prohibit privilege escalation

    However, the new internal security policy now requires the following additional conditions:

        Prohibit running as the root user
        Only allow signed images from a trusted registry (trusted-registry.com)

    Your task is to review the existing Kyverno policies and directly edit the existing policies to meet these new requirements. Do not change the resource names. Once you have completed the edits, update the existing resources in the Kubernetes cluster.
    Steps

        Review and Edit Kyverno Policies
        Directly modify the existing policy resources to meet the new requirements. Ensure that you do not change the names of the resources.

    The cluster's kubeconfig is at `{{ kubeconfig }}`.
    ```

    When an agent is invoked, an input is provided about this scenario. The input is the json following schema. (You can get the exact value by `make get`)
    ```json
    {
        "metadata": {
            "name": "policy-adapt/scenario1", // Scenario Name
            "description": "Kyverno Policy Adapting: Enhancing Policies for Root and Trusted Registry Requirements", // Scenario Description
            "scenario_type": "Upd-CIS-b-K8s-Kyverno" // Scenario Type
        },
        // The above goal description
        "goal_template": "Currently, the following Kyverno policies are deployed in the Kubernetes cluster. Review these existing policies and edit them to meet additional security requirements. Please avoid creating new policy resources; instead, make the necessary changes directly to the existing resources.\n\n    Prohibit the use of the default service account\n    Prohibit privilege escalation\n\nHowever, the new internal security policy now requires the following additional conditions:\n\n    Prohibit running as the root user\n    Only allow signed images from a trusted registry (trusted-registry.com)\n\nYour task is to review the existing Kyverno policies and directly edit the existing policies to meet these new requirements. Do not change the resource names. Once you have completed the edits, update the existing resources in the Kubernetes cluster.\nSteps\n\n    Review and Edit Kyverno Policies\n    Directly modify the existing policy resources to meet the new requirements. Ensure that you do not change the names of the resources. \n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
        "vars": {
            "kubeconfig": "apiVersion: v1\nclusters..." // kubeconfig.yaml contents for access to the target Kubernetes
        }
    }
    ```


1. How it is evaluated

    The evaluation verifies the following to return a pass:
    - Verify that the specified Kyverno policy produces the expected Kyverno policy report for the target resource.
    - Ensure that no modifications have been made to policies that should not be updated, and that no new policies have been created.

    Please refer to [evaluation.py](/ciso/4.upd-cis-b-k8s-kyverno/evaluation.py) for the details.

**The contents of the directory**:
```
├── 4.updating-k8s-kyverno
│   ├── evaluation  # Tools or scripts to check if the injected security issues are detected or not in this scenario
│   ├── manifests   # Kubernetes resources to be deployed for compliance violation 
│   ├── playbooks   # Ansible playbooks to set up the scenario environment
│   ├── examples    # Example Kyverno Policy to detect the compliance violation
│   └── Makefile    # Commands to simplify setup and execution for the scenario
```

## Try Benchmark
1. Start Benchmark Server
1. Start Benchmark Runner
1. Create sample-task-scenarios/ciso/scenario-bundles.json
    ```
    token=`curl -k -s -X POST \
        -H "Content-Type: application/x-www-form-urlencoded" \
        "https://localhost:8000/test/token" \
        -d "username=service_compliance&password=" | jq -r .access_token`
    curl -k -X POST \
        -H "Authorization: Bearer $token" \
        -H "Content-type: application/json" \
        "https://localhost:8000/test/registry/setup-scenarios" -d @sample-task-scenarios/ciso/scenario-bundles.json | jq
    ```
1. Go to Benchmark UI and create agent with Expert level and all categories selected
    ![registration](/ciso/images/registration.png)

1. Run Benchmark and finally obtain these 4 scenarios' scores
    ![registration](/ciso/images/leaderboard.png)

## Usage

Each scenario contains Makefile that contains the following targets. Benchmark Runner invokes these targets.

- deploy_bundle: setup the target environment
- inject_fault: deploy or configure the target environment so it violates the compliance requirement
- get: get the scenario details that would be passed as the input for Agent
- evaluate: valuate
- get_status: get status
- destroy_bundle: delete the target environment
- revert_bundle: revert the target environment

### Pre-requisites (verified only on M1 Mac OSX)
1. Docker runtime (e.g. [Rancher Desktop](https://docs.rancherdesktop.io/getting-started/installation))
1. KinD (tested with 0.19.0)
    - For Rancher Desktop use, some older versions don't work with KinD. We have only tested on Rancher 1.16.0.
1. Kubectl (tested with v1.31.0)
1. Helm (tested with v3.16.1)
    - `brew install helm`
1. [OPA](https://www.openpolicyagent.org/) (tested with v1.0.0)
1. Ansible Playbook (tested with 2.17.4) and kubernetes.core module
    - From Homebrew
        - `brew install ansible`
    - From PyPI
        - `pip install ansible` (see also https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#pipx-install)
        - `ansible-galaxy collection install kubernetes.core`
        - `pip install jmespath kubernetes`
1. jq command
    - `brew install jq`

### Run Task Scenario Manually
1. Go to the directory of a bundle (e.g. `cd 1.gen-cis-b-k8s-kyverno`)
1. Create a scenario environment
    This command creates a Kind Cluster and install Kyverno to the cluster
    - `make deploy_bundle FOREGROUND=true`
1. Inject compliance issues into the environment
    This command deploys nginx that violates the policy to minimize the admission of containers wishing to share the host network namespace. (hostNetwork is set to true)
    - `make inject_fault FOREGROUND=true`
    
    - Now a pod that violates the policy to minimize the admission of containers wishing to share the host network namespace. (hostNetwork is set to true)
        ```
        $ kubectl get pod -n paa
        NAME                                READY   STATUS    RESTARTS   AGE
        nginx-deployment-5778696c59-2j7cb   1/1     Running   0          10m
        ```
        ```
        $ kubectl get pod -n paa nginx-deployment-5778696c59-2j7cb -o yaml
          apiVersion: v1
          kind: Pod
          metadata:
            creationTimestamp: "2025-01-17T06:26:41Z"
          spec:
            containers:
            - image: nginx:1.14.2
              imagePullPolicy: IfNotPresent
              ...
            hostNetwork: true
          ...
        ```
1. Get the goal and invoke your Agent to satisfy the goal
    ```
    $ make get 2>/dev/null
    {
      "metadata": {
        "name": "cis-b.5.2.5-gen",
        "description": "CIS Benchmark for K8S 5.2.5 (Kyverno)",
        "incident_type": "policy_gen",
        "scenario_type": "Gen-CIS-b-K8s-Kyverno",
        "goal": "Minimize the admission of containers wishing to share the host network namespace."
      },
      "goal_template": "I would like to check if the following condition is satisfiled, given a Kubernetes cluster with `kubeconfig.yaml`\n    Minimize the admission of containers wishing to share the host network namespace.\n\nTo check the condition, do the following steps. \n- deploy a Kyverno policy to the cluster\n- chcek if the policy is correctly deployed. \n\nIf deploying the policy failed and if you can fix the issue, you will do it and try deploying again.\nOnce you get a final answer, you can quit the work.\n\nThe cluster's kubeconfig is at `{{ kubeconfig }}`.\n",
      "vars": {
        "kubeconfig": "..."
      }
    }
    ```
1. Once your agent is finished, run evaluation.
    - `make evaluate`
1. Cleanup (delete cluster)
    - `make destroy_bundle`
