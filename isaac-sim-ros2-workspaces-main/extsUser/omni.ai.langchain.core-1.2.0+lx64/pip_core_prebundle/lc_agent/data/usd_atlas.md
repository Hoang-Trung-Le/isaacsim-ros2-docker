# FAQ

General Questions

## General Questions

### What is USD and why should I use it?

USD, or Universal Scene Description, is a framework for encoding and interchanging scalable and hierarchically organized data between digital content creation applications. It involves asset composition with non-destructive editing features aimed at collaborative scene construction. Check the USD documentation's Overview and Purpose section for more details.

### What programming languages are supported?

USD is built on C++ libraries complemented by Python bindings.

### Isn't USD just another file format?

No, USD is more than a file format. Its primary function is to compose scene descriptions from multiple files and formats, delivering a high-performance scenegraph distinct from simply interchanging files like OBJ, FBX, and Alembic.

### What file formats does USD support?

USD supports three main file formats:
- `.usda`: Human-readable UTF-8 text
- `.usdc`: Crate binary for random-access
- `.usd`: Either `.usda` or `.usdc`

It can also interact with Alembic and MaterialX files and be extended via plugins.

### What file format is my .usd file?

A `.usd` file could be in either binary Crate or text format. You can convert between formats without changing any references to these assets.

### What character encoding does .usda support?

The `.usda` format uses UTF-8 encoding.

### How can I convert USD files between binary and text?

You can use `usdcat` with the `--out` and `--usdFormat` flags to convert between formats. For example:

```shell
$ usdcat file.usd --out file.usd --usdFormat usda
```

or to convert to binary:

```shell
$ usdcat file.usd --out file.usdc
```

See the USD documentation on Converting Between Layer Formats for more info.

### What data types are supported?

USD supports a range of data types detailed in the Basic Datatypes for Scene Description section of its documentation. Addition of new basic datatypes via plugin is not possible.

### What does a USD file look like?

Here's a simple example in `.usda` showing references, inheritance, and variants:

```usda
#usda 1.0

class "_class_Planet" {
    bool has_life = False
}

def Xform "SolarSystem" {
    def "Earth" (references = @./planet.usda@</Planet>) {
        bool has_life = True
        string color = "blue"
    }
    ...
}
```

View the USD Tutorials page for more examples and construction demonstrations.

### Subtler Aspects of Scene Description and Composition

#### Should I use SubLayers or References when combining layers?

The choice between SubLayers and References depends on the contents of the layers and the need in the final composition. SubLayers are simpler but have namespace constraints; References can remap and selectively aggregate layers.

#### What happens to 'overs' when their underlying prim is moved?

"Overs" that are orphaned due to moves become ignored in the final composition. It's the responsibility of the user to update references accordingly to avoid losing overrides.

#### When can you delete a reference?

You can only delete composition arcs like references if they were introduced in the same layerStack. Exceptions apply when using variantSets to guide composition.

#### What's the difference between an 'over' and a 'typeless def'?

An `over` is an auxiliary piece of information that applies if an underlying structure exists, whereas a `def` expects that a prim will have a defined type by the end of composition.

#### Why Can't I Instance a Leaf Mesh Prim Directly?

It's technically possible to instance a leaf mesh prim, but the instance would be considered meaningless from a composition, data sharing, and imaging perspective, resulting in an error state in the UsdImaging Hydra scene delegate.

## Build and Runtime Issues

### Why Isn't Python Finding USD Modules?

If you see import errors for USD Python modules, ensure that you've included the correct path in your `PYTHONPATH`:

```shell
$ export PYTHONPATH=$PYTHONPATH:<inst>/lib/python
```

`<inst>` is your installation directory.

### Why Isn't This Plugin Being Built?

USD distribution plugins are disabled by default. Enable them during build configuration.

### Why Isn't My App Finding USD DLLs and Plugins on Windows?

To ensure your app finds USD DLLs and plugins, place them in either the same directory as the executable or in a directory in your Windows PATH. For monolithic builds, see the PXR_BUILD_MONOLITHIC cmake flag.

# UsdShade Material Assignment

Collection-Based Assignment Basics

## Background

In UsdShade as of summer 2017, material assignment is expressed as a relationship that binds a Material to a prim and its descendants. The actual output the renderer consumes'identified by outputs such as `glslfx:surface` or `ri:bxdf`'determines the rendering behavior.

For example, if the `Material /PreviewMaterial` is bound to the root prim `/Bob` and provides a `glslfx:surface` output, but a descendant `/Bob/Geom/Body` binds a `Material /Skin` with an `ri:bxdf` output, the GL renderer should use the `glslfx:surface` from the ancestor, `/Bob`.

## Resolving Hierarchically-bound Materials

```usda
def Material "PreviewMaterial"
{
    outputs:glslfx:surface.connect = </PreviewMaterial/PreviewSurface.outputs:surface>
    def Shader "PreviewSurface"
    { ... }
}

def Material "Skin"
{
    outputs:ri:surface.connect = </Skin/pxrSurface1.outputs:bxdf>
    def Shader "pxrSurface1"
    { ... }
}

def Xform "Bob"
{
    rel material:binding = </PreviewMaterial>
    def Xform "Geom"
    {
        def Mesh "Body"
        {
            rel material:binding = </Skin>
        }
    }
}
```

Two limitations were identified with direct bindings:

1. Direct bindings can't be established for gprims inside instances without breaking the instances.
2. Managing bindings at different granularity is cumbersome, particularly in systems like Katana.

## Collection-Based Assignment Proposal

We propose an additional `material:binding:collection` property for identifying a Material and Collection pair to be bound. The first binding in order takes precedence and multiple collections are typically non-intersecting.

A valid `material:binding:collection:NAME` must target a single Material and Collection. And `NAME` must be a single token.

If a prim has both `material:binding` and `material:binding:collection:XXX`, the direct `material:binding` is weaker, serving as a fallback.

## Example Collection-Based Assignment

Consider a set with `Material` assignments for different parts, authored on an ancestor of the instances they relate to.

```usda
#usda 1.0

over "Office_set"
{
    def Scope "Materials"
    {
        def Material "Default" { ... }
        def Material "PinkPearl" { ... }
        def Material "YellowPaint" { ... }
    }
    ...

    over "Desk_Assembly"
    {
        rel material:binding = </Office_set/Materials/Default>
        rel material:binding:collection:Erasers = [</Office_set/Materials/PinkPearl>, </Office_set/Desk_Assembly/Cup_grp.collection:Erasers>]
        rel material:binding:collection:Shafts = [</Office_set/Materials/YellowPaint>, </Office_set/Desk_Assembly/Cup_grp.collection:Shafts>]
        ...
    }
    ...
}
```

The `Default` Material is the "fallback material".

## Refinements

### Specifying Binding Strength

A `bindMaterialAs` metadatum allows specifying binding strength: `weakerThanDescendants` or `strongerThanDescendants`.

### Material Purpose

`Material Purpose` is proposed with canonical values: `full` and `preview`. Purpose is encoded by the relationship name:

- `material:binding`: Fallback or all-purpose binding.
- `material:binding:preview`: Purpose-restricted, direct, fallback binding.
- `material:binding:collection`: All-purpose, collection-based binding.

## Resolving Bound Material

Material Resolve selects the single `UsdShadeMaterial` for renderable primitives. The process is parameterized by material purpose, ensuring each Material contains all the shading required for the purpose.

## UsdShade API

A new `UsdShadeMaterialBindingAPI` encapsulates all binding-related mutators and queries.

## Analysis of Collection-Based Binding

### Pros

- Matches authoring patterns in Katana and MaterialX.
- Encapsulates grouping information useful for optimizations.
- Provides a formal handoff from modeling to shading.

### Cons

- Substantially more expensive to resolve materials for a single prim.
- Requires efficient, memoized computation for single-prim queries.
- Can increase memory consumption.

## Integration and Remaining Questions

### Performance

Material resolve algorithms must be efficient and potentially memoized to handle the increased complexity.

### Renderer Instancing

Renderers supporting aggregate instancing will need to handle instances with different material sets effectively.

### Material Layering

Material layering interactions with collection-based assignment will need to be addressed in the future.
