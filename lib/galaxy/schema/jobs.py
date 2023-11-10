from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

from pydantic import (
    Extra,
    Field,
    Required,
    UUID4,
)

from galaxy.schema.fields import (
    DecodedDatabaseIdField,
    EncodedDatabaseIdField,
)
from galaxy.schema.schema import (
    DatasetSourceType,
    EncodedDatasetSourceId,
    EntityIdField,
    JobSummary,
    Model,
    UuidField,
)


class JobInputSummary(Model):
    has_empty_inputs: bool = Field(
        default=Required,
        title="Empty inputs",
        description="Job has empty inputs.",
    )
    has_duplicate_inputs: bool = Field(
        default=Required,
        title="Duplicate inputs",
        description="Job has duplicate inputs.",
    )


# TODO: Use Tuple again when `make update-client-api-schema` supports them
class JobErrorSummary(Model):
    # messages: List[Union[Tuple[str, str], List[str]]]
    messages: List[List[str]] = Field(
        default=Required,
        title="Error messages",
        description="The error messages for the specified job.",
    )


class JobAssociation(Model):
    name: str = Field(
        default=Required,
        title="name",
        description="Name of the job parameter.",
    )
    dataset: EncodedDatasetSourceId = Field(
        default=Required,
        title="dataset",
        description="Reference to the associated item.",
    )


class ReportJobErrorPayload(Model):
    dataset_id: DecodedDatabaseIdField = Field(
        default=Required,
        title="History Dataset Association ID",
        description="The History Dataset Association ID related to the error.",
    )
    email: Optional[str] = Field(
        default=None,
        title="Email",
        description="Email address for communication with the user. Only required for anonymous users.",
    )
    message: Optional[str] = Field(
        default=None,
        title="Message",
        description="The optional message sent with the error report.",
    )


class SearchJobsPayload(Model):
    tool_id: str = Field(
        default=Required,
        title="Tool ID",
        description="The tool ID related to the job.",
    )
    # TODO the inputs are actually a dict, but are passed as a JSON dump
    # maybe change it?
    inputs: str = Field(
        default=Required,
        title="Inputs",
        description="The inputs of the job as a JSON dump.",
    )
    state: str = Field(
        default=Required,
        title="State",
        description="The state of the job.",
    )

    class Config:
        extra = Extra.allow  # This is used for items named file_ and __file_


class DeleteJobPayload(Model):
    message: Optional[str] = Field(
        default=None,
        title="Job message",
        description="Stop message",
    )


class EncodedDatasetJobInfo(EncodedDatasetSourceId):
    uuid: UUID4 = UuidField


class EncodedJobIDs(Model):
    id: EncodedDatabaseIdField = EntityIdField
    history_id: Optional[EncodedDatabaseIdField] = Field(
        None,
        title="History ID",
        description="The encoded ID of the history associated with this item.",
    )


class EncodedJobDetails(JobSummary, EncodedJobIDs):
    command_version: str = Field(
        ...,
        title="Command Version",
        description="Tool version indicated during job execution.",
    )
    params: Any = Field(
        ...,
        title="Parameters",
        description=(
            "Object containing all the parameters of the tool associated with this job. "
            "The specific parameters depend on the tool itself."
        ),
    )
    inputs: Dict[str, EncodedDatasetJobInfo] = Field(
        {},
        title="Inputs",
        description="Dictionary mapping all the tool inputs (by name) to the corresponding data references.",
    )
    outputs: Dict[str, EncodedDatasetJobInfo] = Field(
        {},
        title="Outputs",
        description="Dictionary mapping all the tool outputs (by name) to the corresponding data references.",
    )
    # TODO add description, check type and add proper default
    copied_from_job_id: Optional[EncodedDatabaseIdField] = Field(
        default=None, title="Copied from Job-ID", description="Reference to cached job if job execution was cached."
    )
    output_collections: Any = Field(default={}, title="Output collections", description="?")


class JobDestinationParams(Model):
    # TODO add description, check type and add proper default
    runner: str = Field(default=Required, title="Runner", description="Job runner class", alias="Runner")
    runner_job_id: str = Field(
        default=Required,
        title="Runner Job ID",
        description="ID assigned to submitted job by external job running system",
        alias="Runner Job ID",
    )
    handler: str = Field(default=Required, title="Handler", description="?", alias="Handler")


class JobOutput(Model):
    label: Any = Field(default=Required, title="Output label", description="The output label")  # check if this is true
    value: EncodedDatasetSourceId = Field(default=Required, title="dataset", description="The associated dataset.")


class JobParameterValuesSimple(Model):
    src: DatasetSourceType = Field(
        default=Required,
        title="Source",
        description="The source of this dataset, either `hda` or `ldda` depending of its origin.",
    )
    id: EncodedDatabaseIdField = EntityIdField
    name: str = Field(
        default=Required,
        title="Name",
        description="The name of the item.",
    )
    hid: int = Field(
        default=Required,
        title="HID",
        description="The index position of this item in the History.",
    )


class JobTargetElement(Model):  # TODO rename?
    name: str = Field(default=Required, title="Name", description="Name of the element")  # TODO check correctness
    dbkey: str = Field(default=Required, title="Database Key", description="Database key")  # TODO check correctness
    ext: str = Field(default=Required, title="Extension", description="Extension")  # TODO check correctness
    to_posix_lines: bool = Field(
        default=Required, title="To POSIX Lines", description="Flag indicating if to convert to POSIX lines"
    )  # TODO check correctness
    auto_decompress: bool = Field(
        default=Required, title="Auto Decompress", description="Flag indicating if to auto decompress"
    )  # TODO check correctness
    src: str = Field(default=Required, title="Source", description="Source")  # TODO check correctness
    paste_content: str = Field(
        default=Required, title="Paste Content", description="Content to paste"
    )  # TODO check correctness
    hashes: List[str] = Field(default=Required, title="Hashes", description="List of hashes")  # TODO check correctness
    purge_source: bool = Field(
        default=Required, title="Purge Source", description="Flag indicating if to purge the source"
    )  # TODO check correctness
    object_id: EncodedDatabaseIdField = Field(
        default=Required, title="Object ID", description="Object ID"
    )  # TODO check correctness


class JobTargetDestination(Model):
    type: str = Field(
        default=Required,
        title="Type",
        description="Type of destination, either `hda` or `ldda` depending on the destination",
    )  # TODO check correctness


class JobTarget(Model):  # TODO rename?
    destination: JobTargetDestination = Field(
        default=Required, title="Destination", description="Destination details"
    )  # TODO check correctness
    elements: List[JobTargetElement] = Field(
        default=Required, title="Elements", description="List of job target elements"
    )  # TODO check correctness


class JobParameterValuesExtensive(Model):  # TODO rename?
    targets: List[JobTarget] = Field(
        default=Required, title="Targets", description="List of job value targets"
    )  # TODO check correctness
    check_content: bool = Field(
        default=Required, title="Check Content", description="Flag to check content"
    )  # TODO check correctness


class JobParameter(Model):
    text: str = Field(
        default=Required,
        title="Text",
        description="Text associated with the job parameter.",
    )
    depth: int = Field(
        default=Required,
        title="Depth",
        description="The depth of the job parameter.",
    )
    value: Union[List[JobParameterValuesSimple], JobParameterValuesExtensive, str] = Field(
        default=Required, title="Value", description="The values of the job parameter"
    )
    notes: Optional[str] = Field(default=None, title="notes", description="Notes associated with the job parameter.")


class JobDisplayParametersSummary(Model):
    parameters: List[JobParameter] = Field(
        default=Required, title="Parameters", description="The parameters of the job in a nested format."
    )
    has_parameter_errors: bool = Field(
        default=Required, title="Has parameter errors", description="The job has parameter errors"
    )
    outputs: Dict[str, List[JobOutput]] = Field(
        default=Required,
        title="Outputs",
        description="Dictionary mapping all the tool outputs (by name) with the corresponding dataset information in a nested format.",
    )
