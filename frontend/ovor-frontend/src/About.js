import React from 'react';
import './About.css';

function About() {
  return (
    <div className="about-container">
      <header className="about-header">
        <h1>About MGNREGA</h1>
      </header>
      
      <main className="about-content">
        <section className="about-section">
          <h2>What is MGNREGA?</h2>
          <p>
            The Mahatma Gandhi National Rural Employment Guarantee Act (MGNREGA) is a social security measure that aims to guarantee the 'right to work'. 
            The Act was enacted in 2005 and provides at least 100 days of guaranteed wage employment in a financial year to every rural household 
            whose adult members volunteer to do unskilled manual work.
          </p>
        </section>
        
        <section className="about-section">
          <h2>Key Objectives</h2>
          <ul>
            <li>Enhance livelihood security in rural areas</li>
            <li>Create durable assets</li>
            <li>Bring women into the mainstream of economic activities</li>
            <li>Strengthen Panchayati Raj</li>
          </ul>
        </section>
        
        <section className="about-section">
          <h2>How It Works</h2>
          <p>
            Households in rural areas can register for MGNREGA and request work. The Gram Panchayat (village council) is responsible for 
            providing employment within 15 days of receiving an application. If work is not provided within this timeframe, the applicant 
            is entitled to unemployment allowance.
          </p>
        </section>
        
        <section className="about-section">
          <h2>Benefits</h2>
          <div className="benefits-grid">
            <div className="benefit-card">
              <h3>Guaranteed Employment</h3>
              <p>At least 100 days of work per year</p>
            </div>
            <div className="benefit-card">
              <h3>Fair Wages</h3>
              <p>Statutory minimum wages</p>
            </div>
            <div className="benefit-card">
              <h3>Women Empowerment</h3>
              <p>One-third reservation for women</p>
            </div>
            <div className="benefit-card">
              <h3>Dignity of Labour</h3>
              <p>Manual work for rural development</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default About;