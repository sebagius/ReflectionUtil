package dev.agius.minecraft.reflection.mapping;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.*;

public class MappingLoader {
    private final String version;

    public MappingLoader(String version) {
        this.version = version;
        this.classes = new HashMap<>();
    }

    private final Map<String, MappedClass> classes;

    public void loadMappings() {
        Map<String, MappedField> currentFields = new HashMap<>();
        Map<String, MappedMethod> currentMethods = new HashMap<>();
        List<MappedConstructor> currentConstructors = new ArrayList<>();
        String currentClass = null;

        try (InputStreamReader streamReader =
                     new InputStreamReader(getMappingsFile(), StandardCharsets.UTF_8);
             BufferedReader reader = new BufferedReader(streamReader)) {

            String line;
            while ((line = reader.readLine()) != null) {
                if (!line.startsWith("  ")) {
                    if(currentClass != null) {
                        classes.put(currentClass, new MappedClass(currentMethods, currentFields, currentConstructors));
                        currentFields = new HashMap<>();
                        currentMethods = new HashMap<>();
                        currentConstructors = new ArrayList<>();
                    }
                    currentClass = line;
                    continue;
                }

                line = line.substring(2);

                String[] details = line.split(" ");

                /* We are a field */
                if (details.length == 3) {
                    currentFields.put(details[1], new MappedField(details[0], details[2]));
                    continue;
                }

                /* We are a method */
                if (details.length == 4) {
                    currentMethods.put(details[1], new MappedMethod(details[3], details[0], Objects.equals(details[2], "_") ? new String[]{} : details[2].split(",")));
                    continue;
                }

                /* We are a constructor */
                if(details.length == 2 && Objects.equals(details[0], "_")) {
                    currentConstructors.add(new MappedConstructor(details[1].split(",")));
                    continue;
                }
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private InputStream getMappingsFile() {
        return getClass().getClassLoader().getResourceAsStream(version + ".map");
    }

    public Map<String, MappedClass> getClasses() {
        return classes;
    }
}
