/**
 * C# example
 */
public class TestAllLanguages
{
    private string name;

    /**
     * Constructor
     */
    public TestAllLanguages(string name)
    {
        this.name = name;
    }

    /**
     * Return a greeting
     */
    public string Greet()
    {
        return $"Hello, {name}!";
    }
}
