#!/usr/bin/env python3
"""
Update a DNS record. Primary usage as a DDNS client, but also provides
the ablity to update other DNS records.
"""

import argparse
import logging
import dreampylib
import dns.exception
import dns.ipv4
import dns.ipv6
import dns.resolver


LOGGER = logging.getLogger("dh_update_dns")


def main():
    """
    Update a DNS record. Primary usage and DDNS client, but also provides
    the ablity to update other DNS records.
    """
    logging.basicConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument("apikey", help="Your dreamhost API key")
    parser.add_argument("record", help="The record to add/update")
    parser.add_argument(
        "type",
        choices=["A", "CNAME", "NS", "PTR", "NAPTR", "SRV", "TXT", "SPF", "AAAA"],
        help="The type of DNS entry to record",
    )
    parser.add_argument(
        "--value",
        default=None,
        help="The value of the record. If not specified automatically get the \
              current external IP address",
    )
    parser.add_argument(
        "--comment", "-c", help="An optional comment to add to the record"
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Make logging more verbose"
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    else:
        logging.getLogger().setLevel(logging.INFO)

    if args.value is None and (args.type in ["A", "AAAA"]):
        resolver = dns.resolver.Resolver()
        try:
            ip_helper = None
            if args.type == "A":
                ip_helper = dns.ipv4
                resolver.nameservers = [
                    resolver.query("ns1.google.com", "A")[0].to_text()
                ]
            elif args.type == "AAAA":
                resolver.nameservers = [
                    resolver.query("ns1.google.com", "AAAA")[0].to_text()
                ]
                ip_helper = dns.ipv6
            args.value = resolver.query("o-o.myaddr.l.google.com", "TXT")[0].strings[0].decode("utf-8")
            ip_helper.inet_aton(args.value)
        except (dns.resolver.Timeout,
                dns.resolver.NoAnswer,
                dns.resolver.NoNameservers,
                dns.resolver.NXDOMAIN,
                dns.resolver.YXDOMAIN,
                dns.exception.SyntaxError
                ) as exception:
            # "You could have network connectivity problems"
            # or Google retired/changed the service.
            raise Exception("Failed to get external IP address automatically. ", str(exception))

        LOGGER.info("Automatically got IP address: %s", args.value)

    connection = dreampylib.DreampyLib(args.apikey)
    if not connection.is_connected():
        raise Exception("Unable to connect")

    _, _, records = connection.dns.list_records()
    selected = None
    for record in records:
        if record["record"] == args.record and record["type"] == args.type:
            selected = record
            break

    if selected:
        LOGGER.info(
            "Found {record} {type} {value} in the list of existing records, removing it".format(
                **selected
            )
        )
        success, msg, body = connection.dns.remove_record(
            **{
                "record": selected["record"],
                "type": selected["type"],
                "value": selected["value"],
            }
        )
        if not success:
            raise Exception(
                "Failed to remove old record {record} {type} {value}: {msg}. {body}".format(
                    msg=msg, body=body, **selected
                )
            )

    LOGGER.info(
        "Adding {} record {} to Dreamhost with value {}{}".format(
            args.type,
            args.record,
            args.value,
            " and comment " + args.comment if args.comment else "",
        )
    )
    success, msg, body = connection.dns.add_record(
        **{
            "record": args.record,
            "type": args.type,
            "value": args.value,
            "comment": args.comment,
        }
    )
    if not success:
        raise Exception(
            "Failed to create new record {} {} {}: {}. {}".format(
                args.record, args.type, args.value, msg, body
            )
        )

    LOGGER.info("Complete")


if __name__ == "__main__":
    main()
