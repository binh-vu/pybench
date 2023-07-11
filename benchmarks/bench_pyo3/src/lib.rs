mod error;
mod object;

use error::into_pyerr;
use pyo3::{
    prelude::*,
    types::{PyBytes, PyString},
};
use serde::{Deserialize, Serialize};
use std::collections::HashMap;

#[derive(Serialize, Deserialize)]
pub struct RustEntityLabel {
    id: String,
    label: HashMap<String, String>,
}

#[pyfunction]
fn doing_nothing() {}

#[pyfunction]
fn return_5() -> usize {
    5
}

#[pyfunction]
fn get_wikidata_numeric_id(id: &str) -> PyResult<i64> {
    id[1..].parse::<i64>().map_err(into_pyerr)
}

#[pyfunction]
fn get_n_labels(json: &str) -> PyResult<usize> {
    let obj: RustEntityLabel = serde_json::from_str(json).map_err(into_pyerr)?;
    Ok(obj.label.len())
}

#[pyfunction]
fn get_text_len(text: &str) -> PyResult<usize> {
    Ok(text.len())
}

#[pyfunction]
fn uppercase(text: &str) -> PyResult<String> {
    Ok(text.to_uppercase())
}

#[pyfunction]
fn create_numeric_id(id: usize) -> PyResult<object::EntityNumericId> {
    Ok(object::EntityNumericId::new(id))
}

#[pyfunction]
fn create_numeric_id_2(id: usize) -> PyResult<object::FrozenEntityNumericId> {
    Ok(object::FrozenEntityNumericId::new(id))
}

#[pyfunction]
fn is_numeric_id_even(id: usize) -> PyResult<bool> {
    Ok(object::EntityNumericId::new(id).is_even())
}

#[pyfunction]
fn is_numeric_id_even_2(id: usize) -> PyResult<bool> {
    Ok(object::EntityNumericId::new(id).0 % 2 == 0)
}

#[pyfunction]
fn is_numeric_id_even_3(id: usize) -> bool {
    id % 2 == 0
}

#[pymodule]
fn core(py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.setattr("__path__", pyo3::types::PyList::empty(py))?;

    m.add_function(wrap_pyfunction!(doing_nothing, m)?)?;
    m.add_function(wrap_pyfunction!(return_5, m)?)?;
    m.add_function(wrap_pyfunction!(get_wikidata_numeric_id, m)?)?;
    m.add_function(wrap_pyfunction!(get_n_labels, m)?)?;
    m.add_function(wrap_pyfunction!(get_text_len, m)?)?;
    m.add_function(wrap_pyfunction!(uppercase, m)?)?;
    m.add_function(wrap_pyfunction!(create_numeric_id, m)?)?;
    m.add_function(wrap_pyfunction!(create_numeric_id_2, m)?)?;
    m.add_function(wrap_pyfunction!(is_numeric_id_even, m)?)?;
    m.add_function(wrap_pyfunction!(is_numeric_id_even_2, m)?)?;
    m.add_function(wrap_pyfunction!(is_numeric_id_even_3, m)?)?;

    m.add_class::<self::object::EntityLabel>()?;
    m.add_class::<self::object::FrozenEntityLabel>()?;
    m.add_class::<self::object::EntityNumericId>()?;
    m.add_class::<self::object::FrozenEntityNumericId>()?;

    Ok(())
}
