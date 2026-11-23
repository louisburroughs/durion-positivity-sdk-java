package com.positivity.sdk.core;

import java.util.List;

/**
 * Permissions an API operation requires, as published by the backend in the {@code x-required-permissions} and
 * {@code x-required-permissions-all} OpenAPI extensions.
 *
 * <p>The caller must hold every code in {@code allOf} and, when {@code anyOf} is not empty, at least one code in
 * {@code anyOf}. When {@code authenticated} is true the operation needs only a signed-in caller and both lists are
 * empty.
 *
 * <p>An operation that has no entry in a module's {@code OperationRequirements} map has unknown requirements;
 * consumers must treat it as denied (fail closed), never as open.
 *
 * @param anyOf permission codes of which at least one is required
 * @param allOf permission codes that are each required
 * @param authenticated true when any signed-in caller may invoke the operation
 */
public record OperationRequirement(List<String> anyOf, List<String> allOf, boolean authenticated) {

    public OperationRequirement {
        anyOf = List.copyOf(anyOf);
        allOf = List.copyOf(allOf);
    }
}
