export async function getStatus() {
    const res = await fetch("https://your-api-url/api/status", { next: { revalidate: 5 } });
    return res.json();
  }