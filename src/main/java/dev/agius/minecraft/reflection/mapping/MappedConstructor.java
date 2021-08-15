package dev.agius.minecraft.reflection.mapping;

public class MappedConstructor {
    private String[] arguments;

    public MappedConstructor(String[] arguments) {
        this.arguments = arguments;
    }

    public String[] getArguments() {
        return arguments;
    }

    public void setArguments(String[] arguments) {
        this.arguments = arguments;
    }
}
