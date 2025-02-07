# Contributing

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
sample_application: otel_astronomy_shop
```

3. Add any more variables needed for the execution of the tasks.

4. Add the tasks to the `tasks/main.yaml` file. All tasks should have the tag `incident_<number>`, where `<number>` is the number of the new incident. Tasks needed for the fault inject should only run when the variable `is_fault_injection` is true. Tasks needed for fault removal should only run when the variable `is_fault_removal` is true. See the existing tasks for details.

5. Add documentation. See the existing tasks for details. Upon completion, run the following command:

```bash
make documentation
```
