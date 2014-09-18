/*
	wsrmapi.h

	WS-ReliableMessaging plugin.

	See wsrmapi.c for documentation and details.

gSOAP XML Web services tools
Copyright (C) 2000-2010, Robert van Engelen, Genivia Inc., All Rights Reserved.
This part of the software is released under one of the following licenses:
GPL, the gSOAP public license, or Genivia's license for commercial use.
--------------------------------------------------------------------------------
gSOAP public license.

The contents of this file are subject to the gSOAP Public License Version 1.3
(the "License"); you may not use this file except in compliance with the
License. You may obtain a copy of the License at
http://www.cs.fsu.edu/~engelen/soaplicense.html
Software distributed under the License is distributed on an "AS IS" basis,
WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License
for the specific language governing rights and limitations under the License.

The Initial Developer of the Original Code is Robert A. van Engelen.
Copyright (C) 2000-2010, Robert van Engelen, Genivia Inc., All Rights Reserved.
--------------------------------------------------------------------------------
GPL license.

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 2 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, write to the Free Software Foundation, Inc., 59 Temple
Place, Suite 330, Boston, MA 02111-1307 USA

Author contact information:
engelen@genivia.com / engelen@acm.org

This program is released under the GPL with the additional exemption that
compiling, linking, and/or using OpenSSL is allowed.
--------------------------------------------------------------------------------
A commercial use license is available from Genivia, Inc., contact@genivia.com
--------------------------------------------------------------------------------
*/

#ifndef WSRMAPI_H
#define WSRMAPI_H

#include "wsaapi.h"	/* also includes stdsoap2.h, soapH.h */
#include "threads.h"	/* mutex for sequence database */

#ifdef __cplusplus
extern "C" {
#endif

/** Plugin identification for plugin registry */
#define SOAP_WSRM_ID "WS-RM-1.1"

/** Plugin identification for plugin registry */
extern const char soap_wsrm_id[];

/** Max number of retries that soap_wsrm_check_retry can succeed */
#ifndef SOAP_WSRM_MAX_RETRIES
# define SOAP_WSRM_MAX_RETRIES 100
#endif

/** Max seconds to expire a non-terminated sequence and reclaim its resources */
#ifndef SOAP_WSRM_MAX_SEC_TO_EXPIRE
# define SOAP_WSRM_MAX_SEC_TO_EXPIRE 600	/* 10 minutes */
#endif

/** Seconds to timeout when sending ack messages to independent acksto server */
#ifndef SOAP_WSRM_TIMEOUT
# define SOAP_WSRM_TIMEOUT 10
#endif

/**
@enum soap_wsrm_state
@brief wsrm engine state
*/
enum soap_wsrm_enable { SOAP_WSRM_OFF, SOAP_WSRM_ON };

/**
@struct soap_wsrm_data
@brief Plugin data.
*/
struct soap_wsrm_data
{ enum soap_wsrm_enable state;
  struct soap_wsrm_sequence *seq;
  struct soap_wsrm_message *msg;
  int (*fsend)(struct soap*, const char*, size_t);
  int (*fpreparefinalrecv)(struct soap*);
  int (*fdisconnect)(struct soap*);
};

/**
@enum soap_wsrm_message_state
@brief Message state (init, nack or ack)
*/
enum soap_wsrm_message_state { SOAP_WSRM_INIT, SOAP_WSRM_NACK, SOAP_WSRM_ACK };

/**
@struct soap_wsrm_message
@brief Linked list of unacknowledged messages stored for retransmission.
*/
struct soap_wsrm_message
{ ULONG64 num;					/**< message number */
  enum soap_wsrm_message_state state;		/**< (n)ack state */
  struct soap_wsrm_content *list, *last;	/**< list of content blocks */
  struct soap_wsrm_message *next;		/**< next message in list */
};

/**
@struct soap_wsrm_content
@brief L