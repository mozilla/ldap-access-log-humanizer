import re

LDAP_ERROR_CODES = {
    # Indicates the requested client operation completed successfully.
    0: "LDAP_SUCCESS",
    # Indicates that the server has received an invalid or malformed request from the client.
    2: "LDAP_PROTOCOL_ERROR",
    # Indicates that the operation's time limit specified by either the client or the server has been exceeded. On search operations, incomplete results are returned.
    3: "LDAP_TIMELIMIT_EXCEEDED",
    # Indicates that in a search operation, the size limit specified by the client or the server has been exceeded. Incomplete results are returned.
    4: "LDAP_SIZELIMIT_EXCEEDED",
    # Does not indicate an error condition. Indicates that the results of a compare operation are false.
    5: "LDAP_COMPARE_FALSE",
    # Does not indicate an error condition. Indicates that the results of a compare operation are true.
    6: "LDAP_COMPARE_TRUE",
    # Indicates that during a bind operation the client requested an authentication method not supported by the LDAP server.
    7: "LDAP_AUTH_METHOD_NOT_SUPPORTED",
    #  # Indicates one of the following: In bind requests, the LDAP server accepts only strong authentication. In a client request, the client requested an operation such as delete that requires strong authentication. In an unsolicited notice of disconnection, the LDAP server discovers the security protecting the communication between the client and server has unexpectedly failed or been compromised.
    8: "LDAP_STRONG_AUTH_REQUIRED",
    # Does not indicate an error condition. In LDAPv3, indicates that the server does not hold the target entry of the request, but that the servers in the referral field may.
    10: "LDAP_REFERRAL",
    # Indicates that an LDAP server limit set by an administrative authority has been exceeded.
    11: "LDAP_ADMINLIMIT_EXCEEDED",
    # Indicates that the LDAP server was unable to satisfy a request because one or more critical extensions were not available. Either the server does not support the control or the control is not appropriate for the operation type.
    12: "LDAP_UNAVAILABLE_CRITICAL_EXTENSION",
    # Indicates that the session is not protected by a protocol such as Transport Layer Security(TLS), which provides session confidentiality.
    13: "LDAP_CONFIDENTIALITY_REQUIRED",
    # Does not indicate an error condition, but indicates that the server is ready for the next step in the process. The client must send the server the same SASL mechanism to continue the process.
    14: "LDAP_SASL_BIND_IN_PROGRESS",
    # Indicates that the attribute specified in the modify or compare operation does not exist in the entry.
    16: "LDAP_NO_SUCH_ATTRIBUTE",
    # Indicates that the attribute specified in the modify or add operation does not exist in the LDAP server's schema.
    17: "LDAP_UNDEFINED_TYPE",
    # Indicates that the matching rule specified in the search filter does not match a rule defined for the attribute's syntax.
    18: "LDAP_INAPPROPRIATE_MATCHING",
    # Indicates that the attribute value specified in a modify, add, or modify DN operation violates constraints placed on the attribute. The constraint can be one of size or content(string only, no binary).
    19: "LDAP_CONSTRAINT_VIOLATION",
    # Indicates that the attribute value specified in a modify or add operation already exists as a value for that attribute.
    20: "LDAP_TYPE_OR_VALUE_EXISTS",
    # Indicates that the attribute value specified in an add, compare, or modify operation is an unrecognized or invalid syntax for the attribute.
    21: "LDAP_INVALID_SYNTAX",
    # Indicates the target object cannot be found. This code is not returned on following operations: Search operations that find the search base but cannot find any entries that match the search filter. Bind operations.
    32: "LDAP_NO_SUCH_OBJECT",
    # Indicates that an error occurred when an alias was dereferenced.
    33: "LDAP_ALIAS_PROBLEM",
    # Indicates that the syntax of the DN is incorrect. (If the DN syntax is correct, but the LDAP server's structure rules do not permit the operation, the server returns code 53: LDAP_UNWILLING_TO_PERFORM.)
    34: "LDAP_INVALID_DN_SYNTAX",
    # Indicates that the specified operation cannot be performed on a leaf entry. (This code is not currently in the LDAP specifications, but is reserved for this constant.)
    35: "LDAP_IS_LEAF",
    # Indicates that during a search operation, either the client does not have access rights to read the aliased object's name or dereferencing is not allowed.
    36: "LDAP_ALIAS_DEREF_PROBLEM",
    # Indicates that during a bind operation, the client is attempting to use an authentication method that the client cannot use correctly. For example, either of the following cause this error: The client returns simple credentials when strong credentials are required...OR...The client returns a DN and a password for a simple bind when the entry does not have a password defined.
    48: "LDAP_INAPPROPRIATE_AUTH",
    49: "LDAP_INVALID_CREDENTIALS",  # Indicates that during a bind operation one of the following occurred: The client passed either an incorrect DN or password, or the password is incorrect because it has expired, intruder detection has locked the account, or another similar reason. See the data code for more information.
    # Not sure how these will look in logs, commenting them out until we have examples
    # 49 / 52e  AD_INVALID CREDENTIALS  Indicates an Active Directory(AD) AcceptSecurityContext error, which is returned when the username is valid but the combination of password and user credential is invalid. This is the AD equivalent of LDAP error code 49.
    # 49 / 525  USER NOT FOUND  Indicates an Active Directory(AD) AcceptSecurityContext data error that is returned when the username is invalid.
    # 49 / 530  NOT_PERMITTED_TO_LOGON_AT_THIS_TIME   Indicates an Active Directory(AD) AcceptSecurityContext data error that is logon failure caused because the user is not permitted to log on at this time. Returns only when presented with a valid username and valid password credential.
    # 49 / 531  RESTRICTED_TO_SPECIFIC_MACHINES   Indicates an Active Directory(AD) AcceptSecurityContext data error that is logon failure caused because the user is not permitted to log on from this computer. Returns only when presented with a valid username and valid password credential.
    # 49 / 532  PASSWORD_EXPIRED  Indicates an Active Directory(AD) AcceptSecurityContext data error that is a logon failure. The specified account password has expired. Returns only when presented with valid username and password credential.
    # 49 / 533  ACCOUNT_DISABLED  Indicates an Active Directory(AD) AcceptSecurityContext data error that is a logon failure. The account is currently disabled. Returns only when presented with valid username and password credential.
    # 49 / 568  ERROR_TOO_MANY_CONTEXT_IDS  Indicates that during a log-on attempt, the user's security context accumulated too many security IDs. This is an issue with the specific LDAP user object/account which should be investigated by the LDAP administrator.
    # 49 / 701  ACCOUNT_EXPIRED   Indicates an Active Directory(AD) AcceptSecurityContext data error that is a logon failure. The user's account has expired. Returns only when presented with valid username and password credential.
    # 49 / 773  USER MUST RESET PASSWORD  Indicates an Active Directory(AD) AcceptSecurityContext data error. The user's password must be changed before logging on the first time. Returns only when presented with valid user-name and password credential.
    # Indicates that the caller does not have sufficient rights to perform the requested operation.
    50: "LDAP_INSUFFICIENT_ACCESS",
    # Indicates that the LDAP server is too busy to process the client request at this time but if the client waits and resubmits the request, the server may be able to process it then.
    51: "LDAP_BUSY",
    # Indicates that the LDAP server cannot process the client's bind request, usually because it is shutting down.
    52: "LDAP_UNAVAILABLE",
    # Need to sort out above before adding this
    # 52e   AD_INVALID CREDENTIALS  Indicates an Active Directory(AD) AcceptSecurityContext error, which is returned when the username is valid but the combination of password and user credential is invalid. This is the AD equivalent of LDAP error code 49: LDAP_INVALID_CREDENTIALS.
    # Indicates that the LDAP server cannot process the request because of server-defined restrictions. This error is returned for the following reasons: The add entry request violates the server's structure rules...OR...The modify attribute request specifies attributes that users cannot modify...OR...Password restrictions prevent the action...OR...Connection restrictions prevent the action.
    53: "LDAP_UNWILLING_TO_PERFORM",
    # Indicates that the client discovered an alias or referral loop, and is thus unable to complete this request.
    54: "LDAP_LOOP_DETECT",
    # Indicates that the add or modify DN operation violates the schema's structure rules. For example, The request places the entry subordinate to an alias. The request places the entry subordinate to a container that is forbidden by the containment rules. The RDN for the entry uses a forbidden attribute type.
    64: "LDAP_NAMING_VIOLATION",
    65: "LDAP_OBJECT_CLASS_VIOLATION",  # Indicates that the add, modify, or modify DN operation violates the object class rules for the entry. For example, the following types of request return this error: The add or modify operation tries to add an entry without a value for a required attribute. The add or modify operation tries to add an entry with a value for an attribute which the class definition does not contain. The modify operation tries to remove a required attribute without removing the auxiliary class that defines the attribute as required.
    # Indicates that the requested operation is permitted only on leaf entries. For example, the following types of requests return this error: The client requests a delete operation on a parent entry. The client request a modify DN operation on a parent entry.
    66: "LDAP_NOT_ALLOWED_ON_NONLEAF",
    # Indicates that the modify operation attempted to remove an attribute value that forms the entry's relative distinguished name.
    67: "LDAP_NOT_ALLOWED_ON_RDN",
    # Indicates that the add operation attempted to add an entry that already exists, or that the modify operation attempted to rename an entry to the name of an entry that already exists.
    68: "LDAP_ALREADY_EXISTS",
    # Indicates that the modify operation attempted to modify the structure rules of an object class.
    69: "LDAP_NO_OBJECT_CLASS_MODS",
    # Reserved for CLDAP.
    70: "LDAP_RESULTS_TOO_LARGE",
    # Indicates that the modify DN operation moves the entry from one LDAP server to another and requires more than one LDAP server.
    71: "LDAP_AFFECTS_MULTIPLE_DSAS",
    # Indicates an unknown error condition. This is the default value for NDS error codes which do not map to other LDAP error codes.
    80: "LDAP_OTHER",
}


class Operation:
    def __init__(self, op_id):
        self.op_id = op_id
        self.requests = []
        self.response_verb = ""
        self.response_verb_details = set()
        self.error = ""

    def add_error(self, rest):
        # clear prior errors, to make sure we're in sync
        self.error = ""

        # Example: tag=97 err=49 text=
        pattern = r"err=(\d+)"
        match = re.search(pattern, rest)

        # If there was an error, add text error value (so humans can understand)
        if match:
            self.error = LDAP_ERROR_CODES.get(int(match.group(1)))

    def add_event(self, rest):
        verbs = [
            "ADD",
            "MOD",
            "PASSMOD",
            "BIND",
            "SRCH",
            "EXT",
            "STARTTLS",
            "UNBIND",
            "CMP",
            "WHOAMI",
        ]
        tokenized_rest = rest.split(" ")

        if tokenized_rest[0] in verbs:
            # If we get two lines of log output with the same operation and the same verb, it's a continuation,
            # so check if we've already processed one
            if len(self.requests) > 0:
                if tokenized_rest[0] == self.requests[0]["verb"]:
                    # Our splitting on space character doesn't work for attr list in a SRCH operation,
                    # so we need to treat those lines differently, and create a list of attributes
                    if len(tokenized_rest) > 1:
                        if tokenized_rest[1:][0].startswith("attr="):
                            attrs = []
                            for attr in tokenized_rest[1:]:
                                if "=" in attr:
                                    attrs.append(attr.split("=")[1])
                                else:
                                    attrs.append(attr)
                            self.requests[0]["details"].append("attrs=" + ",".join(attrs))
                        else:
                            self.requests[0]["details"].extend(tokenized_rest[1:])
                            self.requests[0]["details"] = list(set(self.requests[0]["details"]))
                else:
                    if len(tokenized_rest) > 1:
                        self.requests.append({"verb": tokenized_rest[0], "details": tokenized_rest[1:]})
            else:
                self.requests.append({"verb": tokenized_rest[0], "details": tokenized_rest[1:]})
        elif tokenized_rest[0] == "RESULT":
            self.response_verb = "RESULT"
            self.response_verb_details.update(tokenized_rest[1:])
        elif tokenized_rest[0] == "SEARCH" and tokenized_rest[1] == "RESULT":
            self.response_verb = "SEARCH RESULT"
            self.response_verb_details.update(tokenized_rest[2:])
        elif tokenized_rest[0] == "ABANDON":
            self.requests.append({"verb": tokenized_rest[0], "details": tokenized_rest[1:]})
            self.response_verb = "None"
        else:
            # This is just a catch all until we exhaust the supported verbs
            raise Exception("Unsupported VERB in: {}".format(rest))

        # Sort the requests details, to make it more deterministic
        for request in self.requests:
            request["details"] = sorted(request["details"])

        self.add_error(rest)

    def dict(self):
        return {
            "op_id": self.op_id,
            "requests": self.requests,
            "response": {
                "verb": self.response_verb,
                "details": sorted(list(self.response_verb_details)),
                "error": self.error,
            },
        }

    def loggable(self):
        # We only want to log op, when we have a result/response
        if self.response_verb == "":
            return False
        else:
            return True
