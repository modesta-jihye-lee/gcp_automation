from __future__ import annotations

import sys
from typing import Any
import hydra
from omegaconf import DictConfig, OmegaConf

from google.api_core.extended_operation import ExtendedOperation
from google.cloud import compute_v1
import google.auth

def wait_for_extended_operation(
    operation: ExtendedOperation, verbose_name: str = "operation", timeout: int = 300
) -> Any:
    """
    Waits for the extended (long-running) operation to complete.

    If the operation is successful, it will return its result.
    If the operation ends with an error, an exception will be raised.
    If there were any warnings during the execution of the operation
    they will be printed to sys.stderr.

    Args:
        operation: a long-running operation you want to wait on.
        verbose_name: (optional) a more verbose name of the operation,
            used only during error and warning reporting.
        timeout: how long (in seconds) to wait for operation to finish.
            If None, wait indefinitely.

    Returns:
        Whatever the operation.result() returns.

    Raises:
        This method will raise the exception received from `operation.exception()`
        or RuntimeError if there is no exception set, but there is an `error_code`
        set for the `operation`.

        In case of an operation taking longer than `timeout` seconds to complete,
        a `concurrent.futures.TimeoutError` will be raised.
    """
    result = operation.result(timeout=timeout)

    if operation.error_code:
        print(
            f"Error during {verbose_name}: [Code: {operation.error_code}]: {operation.error_message}",
            file=sys.stderr,
            flush=True,
        )
        print(f"Operation ID: {operation.name}", file=sys.stderr, flush=True)
        raise operation.exception() or RuntimeError(operation.error_message)

    if operation.warnings:
        print(f"Warnings during {verbose_name}:\n", file=sys.stderr, flush=True)
        for warning in operation.warnings:
            print(f" - {warning.code}: {warning.message}", file=sys.stderr, flush=True)

    return result

def delete_instance(project_id: str, zone: str, machine_name: str) -> None:
    """
    Send an instance deletion request to the Compute Engine API and wait for it to complete.

    Args:
        project_id: project ID or project number of the Cloud project you want to use.
        zone: name of the zone you want to use. For example: “us-west3-b”
        machine_name: name of the machine you want to delete.
    """
    instance_client = compute_v1.InstancesClient()

    print(f"Deleting {machine_name} from {zone}...")
    operation = instance_client.delete(
        project=project_id, zone=zone, instance=machine_name
    )
    wait_for_extended_operation(operation, "instance deletion")
    print(f"Instance {machine_name} deleted.")

def delete_static_ip(project_id, region, address_name):
    address_client = compute_v1.AddressesClient()
    operation_client = compute_v1.RegionOperationsClient()

    operation = address_client.delete(project=project_id, region=region, address=address_name)
    if isinstance(operation, ExtendedOperation):
        operation = operation.result()
    elif hasattr(operation, "name"):
        operation_client.wait(project=project_id, region=region, operation=operation.name)

    print(f"Deleted static IP address: {address_name}")

@hydra.main(version_base=None, config_path='/app/confs', config_name='config.yaml')
def main(cfg:DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    # Basic information
    PROJECT_ID = cfg.basic.project_id
    REGION = cfg.basic.region
    ZONE = cfg.basic.zone
    VM_NAME = cfg.basic.vm_name

    delete_instance(
        project_id=PROJECT_ID,
        zone=ZONE,
        machine_name=VM_NAME,
    )

    if cfg.network.static_ip:
        delete_static_ip(
            project_id=PROJECT_ID,
            region=REGION,
            address_name=VM_NAME
        )

if __name__ == "__main__":
    main()