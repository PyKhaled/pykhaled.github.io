---
title: "Nexus"
date: 2026-09-11
description: "A composable self-hosted application stack exploring reusable infrastructure, explicit configuration, and repeatable deployment packages."
draft: false
tags:
  - engineering
  - developer-tools
  - automation
featured: true
slug: "nexus"
github: "https://github.com/PyKhaled/Nexus"
project_status: "Experimental"
---

## Bringing the stack together

A self-hosted application needs more than its business logic. Authentication, a website, service status, routing, and operational tooling all need to work together. Each service brings its own configuration, dependencies, and release cycle.

Nexus explores how to assemble those capabilities into a coherent system while keeping the individual components replaceable. Its current foundation is a Docker Compose stack with a shared NGINX gateway, supported by configuration tooling and an Assembler that creates deployment packages from blueprints.

## One entry point, independent services

The gateway is the HTTP entry point. It routes requests to applications over a shared Docker network, while backend services keep their application ports internal.

The stack brings together:

- **NGINX** for edge routing and shared gateway policies.
- **Keycloak and PostgreSQL** for authentication.
- **WordPress and MySQL** for the website.
- **Kener and Redis** for service status.
- **Overseer** for observability and control.

The gateway resolves Docker service names when requests arrive. An unavailable upstream can return a gateway error without preventing the gateway itself from starting. This separates gateway availability from the readiness of every application behind it.

## From blueprint to deployment package

The root Compose file defines the local development environment. The Assembler provides a separate path for describing and packaging a selected composition.

A blueprint declares the desired components and can reference independently versioned source repositories. Synchronizing those repositories is an explicit step; planning, validation, and assembly do not silently fetch dependencies.

The workflow is:

1. Declare the composition in a blueprint.
2. Synchronize any required source repositories.
3. Validate the repository inputs.
4. Assemble the deployment package.

This makes the boundary between acquiring dependencies and generating a package visible. Production packages require upstream image digests, while development can use the documented release-tag policy.

## Decisions and tradeoffs

### Compose as the local contract

Keeping one root Compose definition gives local development a clear starting point. Configuration overlays add specific behavior without maintaining a second copy of the whole stack. Other deployment targets need their own lifecycle decisions; they are not automatically interchangeable with Compose.

### Familiar tools for configuration

Make commands and a small Bash helper provide the configuration interface. Runtime values are read as data rather than executed as shell code, and the secret collector rejects duplicate keys. The aim is to keep the workflow inspectable with ordinary files and commands.

### Reuse established applications

Integrating existing applications avoids rebuilding capabilities such as authentication and status pages. The tradeoff is operational: each component still needs upgrades, configuration, and an understanding of its failure modes. Composition organizes that work; it does not remove it.

## Current state

Nexus is experimental. The repository contains the local Compose stack, gateway configuration, Assembler tooling, validation commands, and operational runbooks. The broader product-system model remains a draft, and its capability profile identifies both partial implementations and missing capabilities.

This case study describes the repository's architecture and implementation approach. Production adoption, reliability improvements, and delivery-speed gains have not been established here.

## Explore the implementation

Start with the [repository](https://github.com/PyKhaled/Nexus), browse the [architecture and operations documentation](https://github.com/PyKhaled/Nexus/tree/main/docs), or follow the [open issues](https://github.com/PyKhaled/Nexus/issues) for planned work and acceptance criteria.
