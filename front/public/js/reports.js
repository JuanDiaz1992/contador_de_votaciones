let url2 = 'http://localhost:8000/'; // URL del servidor HTTP

const getCount = () => {
  fetch(`${url2}getCount`, {
    method: "GET",
    mode: 'cors',
  })
  .then((resp) => resp.json())
  .then(data => {
    if (data.data) {
        const countVot = data.count;
        const countys = data.countys
        grafica1(countVot)

/********Validación año con más votaciones***********/
        let electionForYear2000 = countVot.filter((county) => county[1] === 2000);
        let electionForYear2004 = countVot.filter((county) => county[1] === 2004);
        let electionForYear2008 = countVot.filter((county) => county[1] === 2008);
        let electionForYear2012 = countVot.filter((county) => county[1] === 2012);
        let electionForYear2016 = countVot.filter((county) => county[1] === 2016);


        
        let sum2000 = sumVotes(electionForYear2000);
        let sum2004 = sumVotes(electionForYear2004);
        let sum2008 = sumVotes(electionForYear2008);
        let sum2012 = sumVotes(electionForYear2012);
        let sum2016 = sumVotes(electionForYear2016);

        let maxYear = getMaxYear(sum2000, sum2004, sum2008, sum2012, sum2016);

        function sumVotes(countyArray) {
        return countyArray.reduce((total, county) => total + county[2], 0);
        }

        function getMaxYear(...sums) {
        const maxSum = Math.max(...sums);
        if (maxSum === sum2000) {
            return 2000;
        } else if (maxSum === sum2004) {
            return 2004;
        } else if (maxSum === sum2008) {
            return 2008;
        } else if (maxSum === sum2012) {
            return 2012;
        } else if (maxSum === sum2016) {
            return 2016;
        }
        }
            
        let resultList = document.getElementById("listado");

        let listItem2000 = document.createElement("li");
        listItem2000.textContent = `Suma de votos en el año 2000: ${sum2000}`;
        resultList.appendChild(listItem2000);

        let listItem2004 = document.createElement("li");
        listItem2004.textContent = `Suma de votos en el año 2004: ${sum2004}`;
        resultList.appendChild(listItem2004);

        let listItem2008 = document.createElement("li");
        listItem2008.textContent = `Suma de votos en el año 2008: ${sum2008}`;
        resultList.appendChild(listItem2008);

        let listItem2012 = document.createElement("li");
        listItem2012.textContent = `Suma de votos en el año 2012: ${sum2012}`;
        resultList.appendChild(listItem2012);

        let listItem2016 = document.createElement("li");
        listItem2016.textContent = `Suma de votos en el año 2016: ${sum2016}`;
        resultList.appendChild(listItem2016);

        let listItemMaxYear = document.createElement("li");
        listItemMaxYear.textContent = `Año con más votaciones: ${maxYear}`;
        resultList.appendChild(listItemMaxYear);

/***********Validación condado con menos votaciones en el 2018*/
        electionForYear2008.sort((a, b) => a[2] - b[2]);
        let countyWithLeastVotes = electionForYear2008[0][4];
        let con_year = document.getElementById("con_year")
        let county2008 = countys.filter((county) => county[0] === countyWithLeastVotes)
        con_year.textContent  = "Condado con menos votos en el año 2018: " + county2008[0][2];


/*Condados con más votaciones en el partido democrata en los años 2000 al 2008*/     
        let listado2 = document.getElementById("listado2")

        let counts2008ForPartyDemocrat = electionForYear2008.filter((county) => county[3] === "Democrat")
        counts2008ForPartyDemocrat.sort((a, b) => b[2] - a[2])
        let counts20081 = countys.filter((county) => county[0] === counts2008ForPartyDemocrat[0][4])
        let counts20082 = countys.filter((county) => county[0] === counts2008ForPartyDemocrat[1][4])
        let counts20083 = countys.filter((county) => county[0] === counts2008ForPartyDemocrat[2][4])
        
        let listItem2008democtatic1 = document.createElement("li");
        listItem2008democtatic1.textContent = `2008: ${counts20081[0][2]}`;
        listado2.appendChild(listItem2008democtatic1)

        let listItem2008democtatic2 = document.createElement("li");
        listItem2008democtatic2.textContent = `2008: ${counts20082[0][2]}`;
        listado2.appendChild(listItem2008democtatic2)


        let listItem2008democtatic3 = document.createElement("li");
        listItem2008democtatic3.textContent = `2008: ${counts20083[0][2]}`;
        listado2.appendChild(listItem2008democtatic3);


        let listado3 = document.getElementById("listado3")
        let counts2000ForPartyDemocrat = electionForYear2000.filter((county) => county[3] === "Democrat")
        counts2000ForPartyDemocrat.sort((a, b) => a[2] - b[2])
        let counts20001 = countys.filter((count) => count[0] === counts2000ForPartyDemocrat[0][4])
        let counts20002 = countys.filter((count) => count[0] === counts2000ForPartyDemocrat[1][4])
        let counts20003 = countys.filter((count) => count[0] === counts2000ForPartyDemocrat[2][4])
        
        let listItem2000democtatic1 = document.createElement("li");
        listItem2000democtatic1.textContent = `2000: ${counts20001[0][2]}`;
        listado3.appendChild(listItem2000democtatic1)
    
        let listItem2000democtatic12 = document.createElement("li");
        listItem2000democtatic12.textContent = `2000: ${counts20002[0][2]}`;
        listado3.appendChild(listItem2000democtatic12)

        let listItem2000democtatic13 = document.createElement("li");
        listItem2000democtatic13.textContent = `2000: ${counts20003[0][2]}`;
        listado3.appendChild(listItem2000democtatic13)
        
        

/*¿Cuál partido tuvo menos votaciones en el rango de años de 2012 a 2016?*/             
        let counties2012To2016 = countVot.filter(county => county[1] >= 2012 && county[1] <= 2016);
        let partyVotes = {};
        for (let county of counties2012To2016) {
            let party = county[3];
            let votes = county[2];
            if (partyVotes.hasOwnProperty(party)) {
                partyVotes[party] += votes;
            } else {
                partyVotes[party] = votes;
        }}
        let minVotes = Infinity;
        let minParty = "";
        for (let party in partyVotes) {
        if (partyVotes[party] < minVotes) {
            minVotes = partyVotes[party];
            minParty = party;
        }
        }
        let con_party = document.getElementById("con_party")
        con_party.textContent = "Partido con menos votaciones en el rango de 2012 a 2016 es: "+minParty








    }   
    else {
      // No se obtuvieron datos
    }
  })
  .catch(error => {
    console.error("Error fetching county data:", error);
  });
}

(function() {
  getCount()
})();



/*Grafica 1*/         
/*Realice una gráfica donde muestre la comparación del conteo de votaciones por año y por partido.*/
   
const grafica1 = (data_Server) => {
    console.log(data_Server);
  
    const years = [...new Set(data_Server.map(county => county[1]))];
    const parties = [...new Set(data_Server.map(county => county[3]))];
  
    const data = {
      labels: years,
      datasets: parties.map((party, index) => ({
        label: party,
        data: years.map(year => {
            const votes = data_Server
              .filter(county => county[1] === year && county[3] === party)
              .map(county => county[4])
              .reduce((total, vote) => total + vote, 0);
            return votes;
        }),
        backgroundColor: index % 2 === 0 ? 'blue' : 'red',
      })),
    };
  
    // Configuración de la gráfica
    const options = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
        },
        title: {
          display: true,
          text: 'Comparison votes per year and party',
        },
      },
    };
  
    // Crear la gráfica de barras
    const ctx = document.getElementById('myChart1').getContext('2d');
    const myChart = new Chart(ctx, {
      type: 'bar',
      data: data,
      options: options,
    });
  };
  
//   // Datos de ejemplo (puedes reemplazarlo con tus propios datos)
// var data = {
//     labels: ['2018', '2019', '2020', '2021'],
//     datasets: [
//       {
//         label: 'Demócratas',
//         data: [12000, 15000, 18000, 14000],
//         backgroundColor: 'blue'
//       },
//       {
//         label: 'Republicanos',
//         data: [10000, 11000, 13000, 12000],
//         backgroundColor: 'red'
//       },
//       {
//         label: 'Otros',
//         data: [5000, 6000, 7000, 8000],
//         backgroundColor: 'green'
//       }
//     ]
//   };
  
//   // Configuración de la gráfica
//   var options = {
//     responsive: true,
//     maintainAspectRatio: false,
//     scales: {
//       x: {
//         stacked: true
//       },
//       y: {
//         stacked: true
//       }
//     }
//   };
  
//   // Crear la gráfica
//   var ctx = document.getElementById('myChart2').getContext('2d');
//   var myChart = new Chart(ctx, {
//     type: 'bar',
//     data: data,
//     options: options
//   });
  