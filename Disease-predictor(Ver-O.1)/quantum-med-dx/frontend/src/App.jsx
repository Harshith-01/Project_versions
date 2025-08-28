import React from 'react';

const App = () => {
    return (
        <div className="App">
            <header className="App-header">
                <h1>Welcome to Quantum Med DX</h1>
                <p>Your application for advanced medical data processing and quantum computing.</p>
            </header>
            <main>
                <section>
                    <h2>Features</h2>
                    <ul>
                        <li>Data Ingestion</li>
                        <li>Quantum Computing Algorithms</li>
                        <li>Retrieval-Augmented Generation</li>
                        <li>Large Language Model Integration</li>
                    </ul>
                </section>
            </main>
            <footer>
                <p>&copy; {new Date().getFullYear()} Quantum Med DX. All rights reserved.</p>
            </footer>
        </div>
    );
};

export default App;