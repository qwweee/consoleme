# generated by datamodel-codegen:
#   filename:  swagger.yaml
#   timestamp: 2020-07-01T15:04:33+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, constr


class ResourceModel(BaseModel):
    arn: str = Field(..., description="resource ARN")
    account_id: Optional[str] = Field(None, description="AWS account ID")
    account_name: Optional[str] = Field(
        None, description="human-friendly AWS account name"
    )
    policy_sha256: Optional[str] = Field(
        None, description="hash of the most recent resource policy seen by ConsoleMe"
    )
    policy: Optional[str] = None
    owner: Optional[str] = Field(
        None, description="email address of team or individual who owns this resource"
    )
    approvers: Optional[List[str]] = None
    resource_type: Optional[str] = None
    last_updated: Optional[datetime] = Field(
        None, description="last time resource was updated from source-of-truth"
    )


class RequestModel(BaseModel):
    id: str
    arn: str = Field(..., description="ARN of principal being modified")
    timestamp: datetime
    justification: str
    requester_email: str
    approvers: List[str] = Field(
        ...,
        description="list of approvers, derived from approvers of `resource`s in `changes`",
    )
    status: str


class GeneratorType(Enum):
    generic = "generic"
    s3 = "s3"
    sqs = "sqs"
    sns = "sns"


class ChangeGeneratorModel(BaseModel):
    arn: str = Field(..., description="principal ARN")
    generator_type: GeneratorType
    resource: str = Field(..., description="resource ARN")
    version: Optional[str] = Field(None, description="Version")


class AccessLevelEnum(Enum):
    read = "read"
    write = "write"
    list = "list"
    tagging = "tagging"
    permissions_management = "permissions-management"


class GenericChangeGeneratorModel(ChangeGeneratorModel):
    access_level: List[AccessLevelEnum]


class ActionGroup(Enum):
    list = "list"
    get = "get"
    put = "put"
    delete = "delete"


class S3ChangeGeneratorModel(ChangeGeneratorModel):
    bucket_name: Optional[str] = None
    bucket_prefix: Optional[str] = None
    action_groups: List[ActionGroup]


class ActionGroup1(Enum):
    get_queue_attributes = "get_queue_attributes"
    set_queue_attributes = "set_queue_attributes"
    receive_messages = "receive_messages"
    send_messages = "send_messages"
    delete_messages = "delete_messages"


class SQSChangeGeneratorModel(ChangeGeneratorModel):
    action_groups: List[ActionGroup1]


class ActionGroup2(Enum):
    get_topic_attributes = "get_topic_attributes"
    set_topic_attributes = "set_topic_attributes"
    publish = "publish"
    subscribe = "subscribe"
    unsubscribe = "unsubscribe"


class SNSChangeGeneratorModel(ChangeGeneratorModel):
    action_groups: List[ActionGroup2]


class ChangeType(Enum):
    inline_policy = "inline_policy"
    managed_policy = "managed_policy"
    resource_policy = "resource_policy"


class ChangeModel(BaseModel):
    change_type: ChangeType
    resource_arns: List[str]
    resource: Optional[ResourceModel] = None


class Action(Enum):
    attach = "attach"
    detach = "detach"


class ManagedPolicyChangeModel(ChangeModel):
    arn: str
    policy_name: str
    action: Action


class ArnArray(BaseModel):
    __root__: List[
        constr(regex="^arn:([^:]*):([^:]*):([^:]*):(|\*|[\d]{12}|cloudfront|aws):(.+)$")
    ]


class PolicyModel(BaseModel):
    policy_document: str = Field(..., description="JSON policy document")
    policy_sha256: str = Field(..., description="hash of policy_document")


class RoleModel(BaseModel):
    name: str
    account_id: constr(min_length=12, max_length=12)
    account_name: Optional[str] = None
    arn: Optional[str] = None


class CloudTrailError(BaseModel):
    event_call: Optional[str] = None
    count: Optional[int] = None


class CloudTrailErrorArray(BaseModel):
    cloudtrail_errors: Optional[List[CloudTrailError]] = None


class CloudTrailDetailsModel(BaseModel):
    error_url: Optional[str] = None
    errors: Optional[CloudTrailErrorArray] = None


class S3Error(BaseModel):
    error_call: Optional[str] = None
    count: Optional[int] = None
    bucket_name: Optional[str] = None
    request_prefix: Optional[str] = None
    status_code: Optional[int] = None
    status_text: Optional[str] = None
    role_arn: Optional[str] = None


class S3ErrorArray(BaseModel):
    s3_errors: Optional[List[S3Error]] = None


class S3DetailsModel(BaseModel):
    query_url: Optional[str] = None
    error_url: Optional[str] = None
    errors: Optional[S3ErrorArray] = None


class AppDetailsModel(BaseModel):
    name: Optional[str] = None
    owner: Optional[str] = None
    owner_url: Optional[str] = None
    app_url: Optional[str] = None


class AppDetailsArray(BaseModel):
    app_details: Optional[List[AppDetailsModel]] = None


class ExtendedRoleModel(RoleModel):
    inline_policies: List[Dict[str, Any]]
    assume_role_policy_document: Optional[Dict[str, Any]] = None
    cloudtrail_details: Optional[CloudTrailDetailsModel] = None
    s3_details: Optional[S3DetailsModel] = None
    apps: Optional[AppDetailsArray] = None
    managed_policies: List[Dict[str, Any]]
    tags: List[Dict[str, Any]]
    templated: Optional[bool] = None
    template_link: Optional[str] = None


class UserModel(BaseModel):
    email: Optional[str] = None
    extended_info: Optional[Dict[str, Any]] = None
    details_url: Optional[str] = None


class ApiErrorModel(BaseModel):
    status: Optional[int] = None
    title: Optional[str] = None
    message: Optional[str] = None


class Options(BaseModel):
    assume_role_policy: Optional[bool] = False
    tags: Optional[bool] = False
    copy_description: Optional[bool] = False
    description: Optional[str] = None
    inline_policies: Optional[bool] = False
    managed_policies: Optional[bool] = False


class CloneRoleRequestModel(BaseModel):
    account_id: constr(min_length=12, max_length=12)
    role_name: str
    dest_account_id: constr(min_length=12, max_length=12)
    dest_role_name: str
    options: Options


class ActionResult(BaseModel):
    status: Optional[str] = None
    message: Optional[str] = None


class CreateCloneRequestResponse(BaseModel):
    errors: Optional[int] = None
    role_created: Optional[bool] = None
    action_results: Optional[List[ActionResult]] = None


class RoleCreationRequestModel(BaseModel):
    account_id: constr(min_length=12, max_length=12)
    role_name: str
    description: Optional[str] = None
    instance_profile: Optional[bool] = True


class InlinePolicyChangeModel(ChangeModel):
    resource_arns: List[str]
    policy_name: str
    new: bool
    policy: PolicyModel
    old_policy: Optional[PolicyModel] = None


class ResourcePolicyChangeModel(ChangeModel):
    arn: str
    policy: PolicyModel
    old_policy: Optional[PolicyModel] = None


class ChangeModelArray(BaseModel):
    __root__: List[
        Union[
            InlinePolicyChangeModel, ManagedPolicyChangeModel, ResourcePolicyChangeModel
        ]
    ]


class CommentModel(BaseModel):
    id: str
    timestamp: datetime
    edited: Optional[bool] = None
    last_modified: Optional[datetime] = None
    user_email: str
    user: Optional[UserModel] = None
    text: str


class ExtendedRequestModel(RequestModel):
    changes: ChangeModelArray
    requester_info: UserModel
    reviewer: Optional[str] = None
    comments: Optional[CommentModel] = None
