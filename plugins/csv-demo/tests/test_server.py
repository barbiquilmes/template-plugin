import csv

from server import describe_csv_file


def make_csv(tmp_path, rows, headers=None):
    if headers is None:
        headers = ["case_id", "usd_amount"]
    f = tmp_path / "datOh a.csv"
    with open(f, "w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    return str(f)


# --- happy path ---

def test_row_count(tmp_path):
    path = make_csv(tmp_path, [
        {"case_id": "C001", "usd_amount": "100.00"},
        {"case_id": "C002", "usd_amount": "200.00"},
    ])
    assert describe_csv_file(path)["row_count"] == 2


def test_case_ids_preserved_in_order(tmp_path):
    path = make_csv(tmp_path, [
        {"case_id": "C001", "usd_amount": "10"},
        {"case_id": "C002", "usd_amount": "20"},
        {"case_id": "C003", "usd_amount": "30"},
    ])
    assert describe_csv_file(path)["case_ids"] == ["C001", "C002", "C003"]


def test_usd_statistics(tmp_path):
    path = make_csv(tmp_path, [
        {"case_id": "C001", "usd_amount": "100.00"},
        {"case_id": "C002", "usd_amount": "200.50"},
        {"case_id": "C003", "usd_amount": "50.25"},
    ])
    stats = describe_csv_file(path)["usd_amount"]
    assert stats["total"] == 350.75
    assert stats["min"] == 50.25
    assert stats["max"] == 200.50
    assert stats["mean"] == 116.92  # round(350.75 / 3, 2)


def test_extra_columns_are_reported(tmp_path):
    path = make_csv(tmp_path,
        [{"case_id": "C001", "usd_amount": "10", "status": "open"}],
        headers=["case_id", "usd_amount", "status"],
    )
    result = describe_csv_file(path)
    assert "status" in result["columns"]


# --- error cases ---

def test_file_not_found():
    result = describe_csv_file("/nonexistent/path/file.csv")
    assert "error" in result
    assert "not found" in result["error"].lower()


def test_empty_file(tmp_path):
    result = describe_csv_file(make_csv(tmp_path, []))
    assert "error" in result
    assert "empty" in result["error"].lower()


def test_missing_usd_amount_column(tmp_path):
    path = make_csv(tmp_path,
        [{"case_id": "C001", "amount": "100"}],
        headers=["case_id", "amount"],
    )
    result = describe_csv_file(path)
    assert "error" in result
    assert "usd_amount" in result["error"]


def test_missing_case_id_column(tmp_path):
    path = make_csv(tmp_path,
        [{"id": "C001", "usd_amount": "100"}],
        headers=["id", "usd_amount"],
    )
    result = describe_csv_file(path)
    assert "error" in result
    assert "case_id" in result["error"]


def test_invalid_usd_amount(tmp_path):
    path = make_csv(tmp_path, [{"case_id": "C001", "usd_amount": "not_a_number"}])
    result = describe_csv_file(path)
    assert "error" in result
