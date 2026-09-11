# Security policy

This policy covers every repository under
[github.com/pysnmp](https://github.com/pysnmp).

## Reporting a vulnerability

Report privately, through GitHub's private vulnerability reporting, on the
repository the problem is in:

- [pysnmp](https://github.com/pysnmp/pysnmp/security/advisories/new)
- [pysmi](https://github.com/pysnmp/pysmi/security/advisories/new)
- [pyasn1](https://github.com/pysnmp/pyasn1/security/advisories/new)
- [mibs](https://github.com/pysnmp/mibs/security/advisories/new)

If you are not sure which one, report it against
[pysnmp](https://github.com/pysnmp/pysnmp/security/advisories/new) and say so.

Please do not open a public issue, a pull request or a discussion for a
vulnerability. A report that arrives in public is already disclosed, which
takes the choice of timing away from everyone using the library.

Useful reports include the version you tested, the smallest input or
configuration that reproduces the problem, and what an attacker gets out of it.
A packet capture or an encoded PDU is worth more than a description of one.

## What to expect

This is a small, volunteer-maintained project. We aim to acknowledge a report
within a week and to tell you whether we consider it a vulnerability, with
reasoning, once we have looked at it. Fixes ship in a normal release; the
advisory is published when the fix is available, and credits you unless you ask
otherwise.

## Supported versions

Security fixes go to the latest released line of each package. Older lines are
not patched -- there are not enough hands to carry more than one.

## What is not a vulnerability

These libraries implement SNMP, and SNMP is old. Some of what looks alarming is
the protocol working as specified:

- **SNMPv1 and SNMPv2c have no security.** The community string is a cleartext
  password on the wire and there is no integrity protection. That is what those
  versions are. Use SNMPv3 if you need security.
- **SNMPv3 specifies MD5, SHA-1 and DES.** `usmHMACMD5AuthProtocol`,
  `usmHMACSHAAuthProtocol` and `usmDESPrivProtocol` are RFC 3414, and pysnmp
  implements them because deployed equipment speaks them. It warns at run time
  where one is configured. SHA-2 (RFC 7860) and AES (RFC 3826) are available
  and are what you should be configuring.
- **A MIB compiled from an untrusted ASN.1 source is code.** pysmi renders MIB
  modules into Python, and pysnmp imports them. Treat a MIB file from a vendor
  the way you would treat any other source you are about to run.

A report that one of these exists is not a vulnerability report. A report that
one of them is reachable where the configuration says it should not be, or that
a protocol operation can be made to do something the RFC does not allow, is.
