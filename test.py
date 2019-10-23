from manage import app
from flask import json, Flask
import unittest
import requests


class TestApp(unittest.TestCase):

    base_endp = "http://localhost"

    def test_rest_all_data(self):
        data_resp = {"message": "Semua data sukses dihapus"}
        resp = requests.delete(self.base_endp)
        data = resp.json()
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data, data_resp)

    def test_initial_state(self):
        data_resp = {"message": "data kosong"}
        resp = requests.get(self.base_endp)
        data = resp.json()
        self.assertEquals(resp.status_code, 404)
        self.assertEquals(data, data_resp)
        self.assertEquals(data.get("message"), "data kosong")

    def test_get_one_data(self):
        data_resp = {"message": "data kosong"}
        id = 1
        resp = requests.get(self.base_endp + "/{}".format(id))
        data = resp.json()
        self.assertEquals(resp.status_code, 400)
        self.assertEquals(data, data_resp)
        self.assertEquals(data.get("message"), "data kosong")

    def test_post_data(self):
        payload = {
            "judul": "coba yang ini",
            "konten": "ini",
            "featureImage": "imageimage",
        }
        length = 3
        for count in range(length):
            resp = requests.post(self.base_endp, json=payload)
            self.assertEquals(resp.status_code, 200)


if __name__ == "__main__":
    unittest.main()
