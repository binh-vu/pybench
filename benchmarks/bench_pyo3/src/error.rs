use pyo3::PyErr;
use serde_json;
use thiserror::Error;

/// Represent possible errors returned by this library.
#[derive(Error, Debug)]
pub enum BenchPyO3Error {
    #[error(transparent)]
    ParseIntError(#[from] std::num::ParseIntError),

    #[error(transparent)]
    SerdeJsonErr(#[from] serde_json::Error),

    #[error(transparent)]
    PyErr(#[from] pyo3::PyErr),
}

pub fn into_pyerr<E: Into<BenchPyO3Error>>(err: E) -> PyErr {
    let hderr = err.into();
    if let BenchPyO3Error::PyErr(e) = hderr {
        e
    } else {
        let anyerror: anyhow::Error = hderr.into();
        anyerror.into()
    }
}
