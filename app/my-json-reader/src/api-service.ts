// src/api-service.ts
export class ApiService {
  async fetchData(url: string): Promise<any> {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error(`HTTP-Fehler: ${res.status}`);
      return await res.json();
    } catch (err: any) {
      throw new Error(err.message);
    }
  }
}
