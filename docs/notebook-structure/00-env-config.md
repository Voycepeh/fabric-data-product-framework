# `00_env_config`

Shared environment bootstrap and validation before exploration or pipeline notebooks run.

> <a href="https://github.com/Voycepeh/FabricOps-Starter-Kit/blob/main/templates/notebooks/00_env_config.ipynb">Open template notebook</a>

> `00_env_config` is shared setup.

## Segment 1: Explain the shared environment role

Describe what this shared config notebook sets up and what downstream exploration or pipeline notebooks depend on.

## Segment 2: Define environment targets and notebook policy

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/Housepath/"><code>Housepath</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
  </tbody>
</table>

## Segment 3: Set AI, quality, governance, and lineage defaults

## Segment 4: Assemble and validate framework config

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
  </tbody>
</table>

## Segment 5: Run startup checks and show resolved paths

<table class="reference-function-table notebook-structure-function-table">
  <thead>
    <tr>
      <th>Function / class</th>
      <th>Module</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/setup_fabricops_notebook/"><code>setup_fabricops_notebook</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Run consolidated FabricOps startup for exploration and pipeline notebooks.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../api/reference/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
  </tbody>
</table>

