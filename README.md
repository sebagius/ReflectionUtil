# ReflectionUtil

ReflectionUtil is a very basic library which helps users who are using Reflection in later versions of the Minecraft
server. Mojang released their official obfuscation mappings, but since multiple mappings were already created, it made
two sources of mappings for the Minecraft server. Due to this, some fields and methods remain obfuscated in their server
jar while some do not. This tool merges the official Mojang mappings with the obfuscated mappings present in servers
such as `Spigot/Craftbukkit` from versions `1.15` to `1.17.1`.

## Creating the mappings

To create the mappings that can be used with the library you can execute the following commands.

`cd mappingsparser` to change directories to the mapping generator

`python3 main.py` to generate the mappings that are compatible with the library

`cp out/* ../src/main/resources/` to move the mappings to the resources folder.

## Using the library

Once you've created the mappings, go ahead and move everything in the main folder over to your plugin.

Create a new ReflectionUtil instance with the Minecraft version required

`ReflectionUtil reflectionUtil = new ReflectionUtil("1.17.1");`

Load the mappings with `reflectionUtil.getMappingLoader().loadMappings();`

### An Example Getting Fields

For the example, we are going to get the `connection` field in EntityPlayer which has been kept obfuscated as `b` in the
latest server

`reflectionUtil.getField(EntityPlayer.class, "connection");`

This will return a Reflection `Field` object. Under the hood, the mappings are checked and seen that "connection" should
actually be "b" and that field is returned.

### An Example Getting Methods

For the example, we are going to get the `setCamera(Entity)` field in EntityPlayer which has been kept obfuscated as `c`
in the latest server

`reflectionUtil.getMethod(EntityPlayer.class, "setCamera", Entity.class);`

This will return a Reflection `Method` object. Under the hood, the mappings are checked and seen that "setCamera" should
actually be "c" and that method is returned.

#### Notice

- Please notice that this is highly experimental.
- If it is found that the method or field or class does not exist in the mappings, the function will attempt to return
  the regular Object from Reflection
    - Example: if `getName()` does not exist as a mapping, the function will attempt to load the method `getName()`
      instead of any obfuscated method
    - If this regular method does not exist, a MethodNotFoundException will be thrown
- The `getConstructor()` Method just falls through to regular Reflection