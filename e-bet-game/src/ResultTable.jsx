import React, { useState, useEffect } from 'react';
import { useSpring, animated } from 'react-spring';

const ResultTable = () => {
  const [generatedNumbers, setGeneratedNumbers] = useState([]);
  
  useEffect(() => {
    // Simuler la génération des numéros
    const interval = setInterval(() => {
      const newNumber = Math.floor(Math.random() * 100) + 1;
      setGeneratedNumbers((prev) => [...prev, newNumber]);
    }, 1000);

    // Arrêter après 10 numéros
    if (generatedNumbers.length >= 10) {
      clearInterval(interval);
    }

    return () => clearInterval(interval);
  }, [generatedNumbers]);

  return (
    <div className="results-container">
      <h3>Numéros Gagnants :</h3>
      <div className="numbers-list">
        {generatedNumbers.map((number, index) => {
          // Utilisation de React Spring pour animer l'apparition des numéros
          const animationProps = useSpring({
            opacity: 1,
            transform: 'translateX(0)',
            from: { opacity: 0, transform: 'translateX(-50px)' },
            config: { tension: 170, friction: 26 },
            delay: index * 200,  // Delay pour chaque numéro
          });

          return (
            <animated.div key={index} style={animationProps} className="number-item">
              {number}
            </animated.div>
          );
        })}
      </div>
    </div>
  );
};

export default ResultTable;
