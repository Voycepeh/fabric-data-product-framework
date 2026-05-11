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
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/Housepath/"><code>Housepath</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/fabric_input_output/" title="Open fabric_input_output module page" aria-label="Open fabric_input_output module page">fabric_input_output</a></td>
      <td data-label="Purpose">Fabric lakehouse or warehouse connection details.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/validate_framework_config/"><code>validate_framework_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and return a user-supplied framework configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
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
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/validate_framework_config/"><code>validate_framework_config</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Validate and normalize framework configuration input.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/load_fabric_config/"><code>load_fabric_config</code></a></td>
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
      <td data-label="Function / class"><a href="../../reference/step-02b-notebook-startup-checks/run_config_smoke_tests/"><code>run_config_smoke_tests</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Run 00_env_config smoke checks for Spark, runtime context, configured paths, notebook naming, and optional AI/IO imports.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02b-notebook-startup-checks/bootstrap_fabric_env/"><code>bootstrap_fabric_env</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Bootstrap 00_env_config environment readiness by resolving required targets and collecting runtime/AI check results.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/check_fabric_ai_functions_available/"><code>check_fabric_ai_functions_available</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Check whether Fabric AI Functions are available in the current runtime.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-01-governance-context/configure_fabric_ai_functions/"><code>configure_fabric_ai_functions</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Apply optional default Fabric AI Function configuration.</td>
    </tr>
    <tr>
      <td data-label="Function / class"><a href="../../reference/step-02a-shared-runtime-config/get_path/"><code>get_path</code></a></td>
      <td data-label="Module"><a class="reference-module-link" href="../../api/modules/environment_config/" title="Open environment_config module page" aria-label="Open environment_config module page">environment_config</a></td>
      <td data-label="Purpose">Resolve a configured Fabric path for an environment and target.</td>
    </tr>
  </tbody>
</table>

