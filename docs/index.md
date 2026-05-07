# FabricOps Starter Kit

FabricOps Starter Kit is a practical starter kit for building **governed, quality-checked, AI-ready notebooks in Microsoft Fabric**.

It gives teams a reusable way to move from exploration to controlled pipeline delivery with consistent metadata, quality evidence, lineage, and handover artifacts.

## Start here

- [Quick Start](quick-start.md)
- [Lifecycle Operating Model](lifecycle-operating-model.md)
- [Architecture](architecture.md)
- [Storage & Metadata Model](architecture/storage-model.md)
- [Fabric-native Data Quality](architecture/dqx-inspired-fabric-native-dq.md)
- [Notebook Structure](notebook-structure.md)
- [Metadata and Contracts](metadata-and-contracts.md)
- [Function Reference](reference/index.md)
- [Fabric Wheel Install](setup/fabric-wheel-install.md)

## How the starter kit works

- `00_env_config` defines reusable environment settings used across notebooks.
- Exploration notebooks profile and understand data before implementation decisions are finalized.
- Pipeline contract notebooks enforce approved rules and write controlled outputs.
- Metadata, DQ results, lineage, and handover notes are captured as reusable artifacts.

## AI in the loop

- AI assists with metadata summaries, DQ rule suggestions, sensitivity classification suggestions, lineage, and handover notes.
- Humans approve governance and quality decisions.
- Pipeline notebooks enforce approved decisions.

## Architecture pages

- [Platform Architecture](architecture.md) explains the overall workspace and data platform shape.
- [Storage & Metadata Model](architecture/storage-model.md) explains where contracts, profiles, DQ results, lineage, and runtime artifacts live.
- [Fabric-native Data Quality](architecture/dqx-inspired-fabric-native-dq.md) explains the DQX-inspired Fabric-native operating pattern.

## Compatibility note

The Python package import path remains `fabricops_kit`.
