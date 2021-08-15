package dev.agius.minecraft.reflection;

import dev.agius.minecraft.reflection.mapping.*;

import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.Arrays;

public class ReflectionUtil {
    private final MappingLoader mappingLoader;

    public ReflectionUtil(String version) {
        this.mappingLoader = new MappingLoader(version);
    }

    public MappingLoader getMappingLoader() {
        return mappingLoader;
    }

    /**
     *
     * Get a Field object from a Class based on Obfuscation mappings
     *
     * @param clazz the class to request the field from
     * @param fieldName the field that has been obfuscated to attempt to find
     * @return if a matched field is found, that will be returned. Otherwise, the function will attempt to return the field with the requested name
     * @throws NoSuchFieldException when there are no matching fields at all
     */
    public Field getField(Class<?> clazz, String fieldName) throws NoSuchFieldException {
        MappedClass mappedClass = getMappingLoader().getClasses().getOrDefault(clazz.getCanonicalName(), null);
        if(mappedClass == null) {
            return clazz.getField(fieldName);
        }

        MappedField mappedField = mappedClass.getFields().get(fieldName);

        if(mappedField == null) {
            return clazz.getField(fieldName);
        }

        return clazz.getField(mappedField.getObfuscatedName());
    }

    /**
     *
     * Get a Method object from a Class based on Obfuscation mappings
     *
     * @param clazz the class to request the method from
     * @param methodName the method that has been obfuscated to attempt to find
     * @return if a matched method is found, that will be returned. Otherwise, the function will attempt to return the method with the requested name
     * @throws NoSuchMethodException when there are no matching method at all
     */
    public Method getMethod(Class<?> clazz, String methodName, Class<?>... parameters) throws NoSuchMethodException {
        MappedClass mappedClass = getMappingLoader().getClasses().getOrDefault(clazz.getCanonicalName(), null);
        if(mappedClass == null) {
            return clazz.getMethod(methodName, parameters);
        }

        MappedMethod mappedMethod = mappedClass.getMethods().get(methodName);

        if(mappedMethod == null) {
            return clazz.getMethod(methodName, parameters);
        }

        String[] arguments = Arrays.stream(parameters).map(Class::getCanonicalName).toArray(String[]::new);
        if(!Arrays.equals(mappedMethod.getArguments(), arguments)) {
            return clazz.getMethod(methodName, parameters);
        }

        return clazz.getMethod(mappedMethod.getObfuscatedName(), parameters);
    }

    /**
     *
     * Get a Constructor object from a Class based on Obfuscation mappings
     * Note: As constructors are not obfuscated this function falls through to standard reflection
     *
     * @param clazz the class to request the constructor from
     * @return constructor from the class
     * @throws NoSuchMethodException when there are no matching constructors
     */
    public Constructor<?> getConstructor(Class<?> clazz, Class<?>... parameters) throws NoSuchMethodException {
        return clazz.getConstructor(parameters);
    }
}
