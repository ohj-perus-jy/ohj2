# C#-lohkot

<!-- ohj1: vain test_playground.py:n C#-testit käyttävät tätä sivua. Se on
     SUMMARY.md:n ulkopuolella, jotta ohj2:n testit, joissa koekirjan luvut ja
     lohkot on laskettu auki, pysyvät ennallaan; Zensical kääntää sen silti
     kuten ohj1:n omat SUMMARY:n ulkopuoliset sivut. -->

## Ajettava ohjelma

```csharp
//-using System;
//-public class Hei
//-{
//-    public static void Main()
//-    {
        Console.WriteLine("Hei, maailma!");
//-    }
//-}
```

## Ohjelma ilman ajonappia

```csharp,ignore
Console.WriteLine("Tätä ei voi ajaa.");
```

## Jypeli-peli

```csharp,feature-jypeli
using Jypeli;
public class Peli : PhysicsGame
{
    public override void Begin()
    {
        Add(new GameObject(50, 50));
    }
}
```
