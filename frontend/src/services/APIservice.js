const proxy = 'http://localhost:5000'

export default class APIservice {
  static async GetMnistJob() {
    const resp = await fetch(`${proxy}/get_mnist_job`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });
    return await resp.json();
  }

  static async UpdateMnistJob(id, body) {
    const resp = await fetch(`${proxy}/update_mnist_job/${id}`, {
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
    const resp = await fetch(`${proxy}/add_mnist_job`, {
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
    const resp = await fetch(`${proxy}/delete_mnist_job/${id}`, {
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
