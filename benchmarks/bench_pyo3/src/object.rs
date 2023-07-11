use crate::error::into_pyerr;
use hashbrown::HashMap;
use pyo3::prelude::*;
use serde::{Deserialize, Serialize};

#[pyclass]
pub struct EntityNumericId(pub usize);

#[pymethods]
impl EntityNumericId {
    #[new]
    pub fn new(id: usize) -> Self {
        Self(id)
    }

    pub fn is_even(&self) -> bool {
        self.0 % 2 == 0
    }
}

#[pyclass(frozen)]
pub struct FrozenEntityNumericId(usize);

#[pymethods]
impl FrozenEntityNumericId {
    #[new]
    pub fn new(id: usize) -> Self {
        Self(id)
    }
}

#[pyclass]
#[derive(Serialize, Deserialize)]
pub struct EntityLabel {
    id: String,
    label: HashMap<String, String>,
}

#[pymethods]
impl EntityLabel {
    #[staticmethod]
    fn from_json(json: &str) -> PyResult<Self> {
        serde_json::from_str(json).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to parse JSON: {}", e))
        })
    }

    fn doing_nothing(&self) {}

    fn return_5(&self) -> usize {
        5
    }

    fn get_wikidata_numeric_id(&self) -> PyResult<i64> {
        self.id[1..].parse::<i64>().map_err(into_pyerr)
    }

    fn get_n_labels(&self) -> usize {
        self.label.len()
    }
}

#[pyclass]
#[derive(Serialize, Deserialize)]
pub struct FrozenEntityLabel {
    id: String,
    label: HashMap<String, String>,
}

#[pymethods]
impl FrozenEntityLabel {
    #[staticmethod]
    fn from_json(json: &str) -> PyResult<Self> {
        serde_json::from_str(json).map_err(|e| {
            PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Failed to parse JSON: {}", e))
        })
    }

    fn doing_nothing(&self) {}

    fn return_5(&self) -> usize {
        5
    }

    fn get_wikidata_numeric_id(&self) -> PyResult<i64> {
        self.id[1..].parse::<i64>().map_err(into_pyerr)
    }

    fn get_n_labels(&self) -> usize {
        self.label.len()
    }
}
