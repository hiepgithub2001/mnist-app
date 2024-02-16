export default class APIservice {
  static async GetMnistJob() {
    const resp = await fetch(`/get`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });
    console.log(resp);
    return await resp.json();
  }

  static async UpdateMnistJob(id, body) {
    const resp = await fetch(`/update/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      credentials: 'include',
    });
    return await resp.json();
  }

  static async AddMnistJob(body) {
    const resp = await fetch(`/add`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      credentials: 'include',
    });
    return await resp.json();
  }

  static async DeleteMnistJob(id, body) {
    const resp = await fetch(`/delete/${id}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
      credentials: 'include',
    });
    return await resp.json();
  }
}
