# Callable Map

This page is generated from FabricOps source code using static AST parsing. It shows module dependencies, public callables, internal helpers, and cross-module calls.

## 1. Module dependency graph

```mermaid
flowchart LR
  config --> metadata
```

## 2. Public callables by module

| Module | Public callable | Referenced by |
|---|---|---|
| `config` | `load_config` | — |

## 3. Internal helper index

| Module | Internal helper | Called by public callables |
|---|---|---|
| `config` | `_validate_runtime_environment` | `fabricops_kit.config.load_config` |

## 4. Cross-module FabricOps calls

| Caller | Callee | Callee kind |
|---|---|---|
| `fabricops_kit.config.load_config` | `fabricops_kit.metadata.resolve_env_profile` | `internal_callable` |

## 5. Module dependency summary

| Module | Calls modules | Called by modules | Public callables | Internal helpers |
|---|---|---|---:|---:|
| `config` | `metadata` | — | 1 | 1 |
