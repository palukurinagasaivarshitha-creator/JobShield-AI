/**
 * Frontend API Service for Fake Job Detection & Verification Platform
 * All calls route through Vite development proxy or relative /api endpoints.
 */

const BASE_URL = 'https://jobshield-ai-1-rxez.onrender.com/api';

async function handleResponse(response) {
  if (!response.ok) {
    let errorDetail = 'Network request failed';
    try {
      const errJson = await response.json();
      errorDetail = errJson.detail || errJson.message || errorDetail;
    } catch {
      errorDetail = `${response.status} ${response.statusText}`;
    }
    throw new Error(errorDetail);
  }
  return response.json();
}

export const api = {
  // System Health
  async getHealth() {
    const res = await fetch(`${BASE_URL}/health`);
    return handleResponse(res);
  },

  // Dashboard Overview
  async getDashboardStats() {
    const res = await fetch(`${BASE_URL}/jobs/dashboard/stats`);
    return handleResponse(res);
  },

  // Comprehensive Multi-Vector Job Analysis
  async analyzeJob(payload) {
    const res = await fetch(`${BASE_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    return handleResponse(res);
  },

  // Safe Job URL Metadata Extraction
  async extractJobUrl(url) {
    const res = await fetch(`${BASE_URL}/extract`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    return handleResponse(res);
  },

  // Standalone Company & Domain Verification
  async verifyCompany(companyName, jobUrl = null) {
    const res = await fetch(`${BASE_URL}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ company_name: companyName, job_url: jobUrl }),
    });
    return handleResponse(res);
  },

  // Search Jobs & Verified Listings
  async searchJobs(query = '', classification = '', limit = 12, offset = 0) {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (classification) params.append('classification', classification);
    params.append('limit', limit);
    params.append('offset', offset);

    const res = await fetch(`${BASE_URL}/jobs/search?${params.toString()}`);
    return handleResponse(res);
  },

  // Audit History
  async getHistory(query = '', classification = '', limit = 20, offset = 0) {
    const params = new URLSearchParams();
    if (query) params.append('q', query);
    if (classification) params.append('classification', classification);
    params.append('limit', limit);
    params.append('offset', offset);

    const res = await fetch(`${BASE_URL}/history?${params.toString()}`);
    return handleResponse(res);
  },

  async getHistoryDetail(id) {
    const res = await fetch(`${BASE_URL}/history/${id}`);
    return handleResponse(res);
  },

  async deleteHistory(id) {
    const res = await fetch(`${BASE_URL}/history/${id}`, {
      method: 'DELETE',
    });
    return handleResponse(res);
  },
};


