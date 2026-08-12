# Durion Positivity Java SDK

Generated Java client SDK for the Durion Positivity backend APIs. Each module provides a type-safe RestTemplate-based HTTP client for one backend domain, auto-generated from the corresponding OpenAPI spec.

## Requirements

| Dependency  | Version |
| ----------- | ------- |
| Java        | 25      |
| Spring Boot | 4.0.6   |
| Maven       | 3.9+    |

The `durion-positivity-backend` repository must be checked out as a sibling directory — module poms resolve OpenAPI specs via relative paths (`../../durion-positivity-backend/<module>/openapi.yaml`).

## Modules

| Artifact                     | Package prefix                        | Backend spec                         |
| ---------------------------- | ------------------------------------- | ------------------------------------ |
| `sdk-java-accounting`        | `com.positivity.sdk.accounting`       | `pos-accounting/openapi.yaml`        |
| `sdk-java-bulk-loader`       | `com.positivity.sdk.bulkloader`       | `pos-bulk-loader/openapi.yaml`       |
| `sdk-java-catalog`           | `com.positivity.sdk.catalog`          | `pos-catalog/openapi.yaml`           |
| `sdk-java-customer`          | `com.positivity.sdk.customer`         | `pos-customer/openapi.yaml`          |
| `sdk-java-documents`         | `com.positivity.sdk.documents`        | `pos-documents/openapi.yaml`         |
| `sdk-java-event-receiver`    | `com.positivity.sdk.eventreceiver`    | `pos-event-receiver/openapi.yaml`    |
| `sdk-java-image`             | `com.positivity.sdk.image`            | `pos-image/openapi.yaml`             |
| `sdk-java-inquiry`           | `com.positivity.sdk.inquiry`          | `pos-inquiry/openapi.yaml`           |
| `sdk-java-inventory`         | `com.positivity.sdk.inventory`        | `pos-inventory/openapi.yaml`         |
| `sdk-java-invoice`           | `com.positivity.sdk.invoice`          | `pos-invoice/openapi.yaml`           |
| `sdk-java-location`          | `com.positivity.sdk.location`         | `pos-location/openapi.yaml`          |
| `sdk-java-marketing`         | `com.positivity.sdk.marketing`        | `pos-marketing/openapi.yaml`         |
| `sdk-java-mcp-server`        | `com.positivity.sdk.mcpserver`        | `pos-mcp-server/openapi.yaml`        |
| `sdk-java-order`             | `com.positivity.sdk.order`            | `pos-order/openapi.yaml`             |
| `sdk-java-people`            | `com.positivity.sdk.people`           | `pos-people/openapi.yaml`            |
| `sdk-java-people-contact`    | `com.positivity.sdk.peoplecontact`    | `pos-people-contact/openapi.yaml`    |
| `sdk-java-price`             | `com.positivity.sdk.price`            | `pos-price/openapi.yaml`             |
| `sdk-java-security`          | `com.positivity.sdk.security`         | `pos-security/openapi.yaml`          |
| `sdk-java-shop-manager`      | `com.positivity.sdk.shopmanager`      | `pos-shop-manager/openapi.yaml`      |
| `sdk-java-supplier`          | `com.positivity.sdk.supplier`         | `pos-supplier/openapi.yaml`          |
| `sdk-java-tax`               | `com.positivity.sdk.tax`              | `pos-tax/openapi.yaml`               |
| `sdk-java-vehicle-fitment`   | `com.positivity.sdk.vehiclefitment`   | `pos-vehicle-fitment/openapi.yaml`   |
| `sdk-java-vehicle-inventory` | `com.positivity.sdk.vehicleinventory` | `pos-vehicle-inventory/openapi.yaml` |
| `sdk-java-warranty`          | `com.positivity.sdk.warranty`         | `pos-warranty/openapi.yaml`          |
| `sdk-java-workorder`         | `com.positivity.sdk.workorder`        | `pos-workorder/openapi.yaml`         |

Each module exposes two packages:

- `com.positivity.sdk.<domain>.api` — generated API client classes (`*Api.java`)
- `com.positivity.sdk.<domain>.model` — generated request/response model classes

## Build

Build all modules:

```bash
mvn compile
```

Build a single module:

```bash
mvn compile -pl sdk-java-workorder
```

Code generation runs automatically during `compile` via the `openapi-generator-maven-plugin`. Generated sources are written to `<module>/target/generated-sources/openapi/`.

## Code formatting

Formatting is enforced by the [Spotless Maven plugin](https://github.com/diffplug/spotless) (v2.43.0) using [Palantir Java Format](https://github.com/palantir/palantir-java-format) (v2.90.0).

Apply formatting to all modules:

```bash
mvn spotless:apply
```

Check formatting without modifying files (exits non-zero if any file is out of format):

```bash
mvn spotless:check
```

Scope either command to a single module with `-pl`:

```bash
mvn spotless:apply -pl sdk-java-workorder
```

`spotless:apply` is bound to the `process-sources` phase, so it runs automatically after code generation during any `mvn compile` (or later lifecycle goal). Generated sources under `target/generated-sources/` are formatted in the same pass as hand-written sources in `src/main/java/`.

Run `spotless:check` in CI to reject unformatted code.

## Usage

Add individual module dependencies to your `pom.xml`:

```xml
<dependency>
    <groupId>com.positivity</groupId>
    <artifactId>sdk-java-workorder</artifactId>
    <version>0.1.0-SNAPSHOT</version>
</dependency>
```

Each module's `ApiClient` is a Spring `@Component` and can be injected directly. Configure the base URL before use:

```java
@Autowired
private ApiClient apiClient;

@Autowired
private WorkordersApi workordersApi;

@PostConstruct
void configure() {
    apiClient.setBasePath("https://api.example.com");
}
```

`ApiClient` accepts a `RestTemplate` instance via its constructor, making it straightforward to plug in your application's configured `RestTemplate` (with auth interceptors, timeouts, etc.).

## Architecture

All modules share a single parent POM at the repository root. Generation options applied across every module:

| Option               | Value                              |
| -------------------- | ---------------------------------- |
| Generator            | `java` (RestTemplate library)      |
| Jakarta EE           | enabled (`useJakartaEe=true`)      |
| Nullable wrapper     | disabled (`openApiNullable=false`) |
| Date library         | `java8`                            |
| Serializable models  | enabled                            |
| Unknown enum default | enabled                            |

### Custom ApiClient template

`templates/libraries/resttemplate/ApiClient.mustache` overrides the upstream generator template to restore compatibility with Spring Framework 7 (shipped with Spring Boot 4). The upstream template called two `HttpHeaders` API methods removed in Spring 7:

- `HttpHeaders.containsKey()` → replaced with `HttpHeaders.set()` (deduplicate-then-add → direct set)
- `HttpHeaders.entrySet()` → replaced with `HttpHeaders.forEach()` lambda

The override file is minimal — only `ApiClient.mustache` is customised; all other templates are sourced from the generator JAR.

## Generating and regenerating source code

Source code is generated automatically by the `openapi-generator-maven-plugin` during the Maven `generate-sources` phase, which runs as part of `compile`. The plugin reads each module's configured OpenAPI spec and writes Java source files into `target/generated-sources/openapi/src/main/java/`.

### How generation works

1. The plugin binds to the `generate-sources` lifecycle phase.
2. It reads the input spec declared in the module's `pom.xml` (e.g. `../../durion-positivity-backend/pos-accounting/openapi.yaml`).
3. It writes generated Java source files into `<module>/target/generated-sources/openapi/`.
4. Maven's `compile` phase then compiles those sources alongside any hand-written code.

Generated sources are **not committed** to version control — they are produced fresh on every build.

### Generate all modules

```bash
mvn generate-sources
```

Or trigger generation as part of a full compile:

```bash
mvn compile
```

### Generate a single module

```bash
mvn generate-sources -pl sdk-java-workorder
```

Replace `sdk-java-workorder` with any module name from the [Modules](#modules) table.

### Regenerate after a spec change

Maven's incremental build may skip generation if it thinks sources are up to date. Use `clean` to force a full regeneration:

```bash
# Regenerate one module
mvn clean generate-sources -pl sdk-java-workorder

# Regenerate all modules
mvn clean generate-sources
```

`clean` deletes each module's `target/` directory, ensuring the generator runs unconditionally.

### Verify generated output

After generation, sources are available at:

```text
sdk-java-<module>/
└── target/
    └── generated-sources/
        └── openapi/
            └── src/main/java/
                └── com/positivity/sdk/<domain>/
                    ├── api/          # *Api.java — one class per API tag
                    ├── model/        # request/response POJOs
                    └── ApiClient.java
```

### Prerequisites for generation

- The `durion-positivity-backend` repository must be checked out as a sibling of this repository, since specs are resolved via relative paths:

  ```text
  parent-dir/
  ├── durion-positivity-sdk-java/   ← this repo
  └── durion-positivity-backend/    ← required sibling
  ```

- Java 25 and Maven 3.9+ must be on `PATH`.

## Repository layout

```text
durion-positivity-sdk-java/
├── pom.xml                         # parent POM — versions, shared deps, plugin management
├── templates/
│   └── libraries/resttemplate/
│       └── ApiClient.mustache      # Spring 7 compatible override
├── sdk-java-accounting/
│   └── pom.xml                     # module POM — points to backend openapi.yaml
├── sdk-java-workorder/
│   └── pom.xml
└── ...                             # one directory per domain module
```

Generated sources appear under each module's `target/` directory and are not committed to version control.
