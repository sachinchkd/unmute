import { useState } from "react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";

const API_BASE = import.meta.env.VITE_API_BASE_URL || "";

type LengthOption = "short" | "medium" | "long" | "extra_long";

function App() {
  const [paragraphs, setParagraphs] = useState(3);
  const [length, setLength] = useState<LengthOption>("medium");
  const [output, setOutput] = useState("");
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState("");

  async function generateText() {
    setLoading(true);
    setError("");
    setCopied(false);

    try {
      const safeParagraphs = Math.min(Math.max(paragraphs, 1), 10);

      const params = new URLSearchParams({
        paragraphs: String(safeParagraphs),
        length,
      });

      const response = await fetch(`${API_BASE}/api/generate?${params}`);

      if (!response.ok) {
        throw new Error("Failed to generate text");
      }

      const data: { text: string } = await response.json();
      setOutput(data.text);
    } catch {
      setError("Could not generate text. Make sure FastAPI is running.");
    } finally {
      setLoading(false);
    }
  }

  async function copyText() {
    if (!output) return;

    await navigator.clipboard.writeText(output);
    setCopied(true);

    setTimeout(() => {
      setCopied(false);
    }, 1200);
  }

  return (
    <main className="min-h-screen bg-zinc-50 px-4 py-10 text-zinc-950">
      <section className="mx-auto max-w-5xl">
        <div className="mb-8 text-center">
          <p className="mb-3 text-xs font-black uppercase tracking-[0.25em] text-zinc-500">
            Unofficial Devanagari Ipsum Generator
          </p>

          <h1 className="text-5xl font-black tracking-tight sm:text-7xl md:text-8xl">
            Balen Bolcha
          </h1>

          <p className="mx-auto mt-5 max-w-2xl text-base leading-8 text-zinc-600 sm:text-lg">
            Generate Devanagari-style filler text using your trained Markov
            chain model.
          </p>
        </div>

        <Card className="rounded-3xl border-zinc-200 shadow-xl">
          <CardHeader>
            <CardTitle className="text-2xl">Generate Text</CardTitle>
            <CardDescription>
              Choose paragraph count and length, then generate filler text.
            </CardDescription>
          </CardHeader>

          <CardContent className="space-y-5">
            <div className="grid gap-4 md:grid-cols-[1fr_1fr_auto] md:items-end">
              <div className="space-y-2">
                <Label htmlFor="paragraphs">Paragraphs</Label>
                <Input
                  id="paragraphs"
                  type="number"
                  min={1}
                  max={10}
                  value={paragraphs}
                  onChange={(event) =>
                    setParagraphs(Number(event.target.value))
                  }
                />
              </div>

              <div className="space-y-2">
                <Label>Length</Label>
                <Select
                  value={length}
                  onValueChange={(value) => setLength(value as LengthOption)}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select length" />
                  </SelectTrigger>

                  <SelectContent>
                    <SelectItem value="short">Short</SelectItem>
                    <SelectItem value="medium">Medium</SelectItem>
                    <SelectItem value="long">Long</SelectItem>
                    <SelectItem value="extra_long">Extra Long</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Button onClick={generateText} disabled={loading}>
                {loading ? "Generating..." : "Generate"}
              </Button>
            </div>

            {error && (
              <p className="rounded-xl bg-red-100 px-4 py-3 text-sm font-semibold text-red-700">
                {error}
              </p>
            )}

            <Textarea
              value={output}
              onChange={(event) => setOutput(event.target.value)}
              placeholder="Generated text will appear here..."
              className="min-h-[380px] resize-y bg-zinc-50 text-lg leading-9"
            />

            <div className="flex justify-end">
              <Button variant="secondary" onClick={copyText} disabled={!output}>
                {copied ? "Copied!" : "Copy Text"}
              </Button>
            </div>
          </CardContent>
        </Card>

        <p className="mx-auto mt-6 max-w-2xl text-center text-sm leading-6 text-zinc-500">
          This is an unofficial parody/filler-text generator. It is not
          affiliated with or endorsed by the original public figure.
        </p>
      </section>
    </main>
  );
}

export default App;