/* =======================================================
   THEME TOGGLE
======================================================= */

const themeBtn =
document.getElementById('themeBtn');

themeBtn.addEventListener('click',()=>{

  document.body.classList.toggle('light');

  if(document.body.classList.contains('light')){

    themeBtn.innerHTML = '🌙';

  }else{

    themeBtn.innerHTML = '☀️';
  }

});

/* =======================================================
   CANVAS
======================================================= */

const canvas =
document.getElementById('canvas');

const ctx =
canvas.getContext('2d');

let w =
canvas.width = window.innerWidth;

let h =
canvas.height = window.innerHeight;

/* =======================================================
   MOUSE
======================================================= */

const mouse = {

  x:w/2,
  y:h/2,
  radius:180
};

const glow =
document.getElementById('glow');

/* =======================================================
   RESIZE
======================================================= */

window.addEventListener('resize',()=>{

  w = canvas.width =
  window.innerWidth;

  h = canvas.height =
  window.innerHeight;

});

/* =======================================================
   MOUSE MOVE
======================================================= */

window.addEventListener('mousemove',(e)=>{

  mouse.x = e.clientX;
  mouse.y = e.clientY;

  glow.style.left =
  e.clientX + 'px';

  glow.style.top =
  e.clientY + 'px';

});

/* =======================================================
   PARTICLE
======================================================= */

class Particle{

  constructor(){

    this.baseX = Math.random()*w;
    this.baseY = Math.random()*h;

    this.x = this.baseX;
    this.y = this.baseY;

    this.size = Math.random()*2.5 + 1;

    this.vx = 0;
    this.vy = 0;

    this.angle =
    Math.random()*Math.PI*2;

    this.speed =
    Math.random()*0.01 + 0.003;
  }

  draw(){

    ctx.beginPath();

    ctx.arc(
      this.x,
      this.y,
      this.size,
      0,
      Math.PI*2
    );

    const color =
    document.body.classList.contains('light')
    ?
    'rgba(90,90,255,0.85)'
    :
    'rgba(255,255,255,0.95)';

    ctx.fillStyle = color;

    ctx.fill();
  }

  update(time){

    this.angle += this.speed;

    this.baseX +=
    Math.cos(this.angle) * 0.15;

    this.baseY +=
    Math.sin(this.angle) * 0.15;

    let dx = mouse.x - this.x;
    let dy = mouse.y - this.y;

    let distance =
    Math.sqrt(dx*dx + dy*dy);

    if(distance < mouse.radius){

      let force =
      (mouse.radius - distance)
      / mouse.radius;

      let angle =
      Math.atan2(dy,dx);

      this.vx -=
      Math.cos(angle) * force * 2;

      this.vy -=
      Math.sin(angle) * force * 2;
    }

    let waveX =
    Math.sin(
      time * 0.001 +
      this.baseY * 0.01
    ) * 15;

    let waveY =
    Math.cos(
      time * 0.001 +
      this.baseX * 0.01
    ) * 15;

    this.vx *= 0.94;
    this.vy *= 0.94;

    this.x +=
    this.vx +
    ((this.baseX + waveX)
    - this.x) * 0.04;

    this.y +=
    this.vy +
    ((this.baseY + waveY)
    - this.y) * 0.04;

    this.draw();
  }
}

/* =======================================================
   CREATE PARTICLES
======================================================= */

const particles = [];

for(let i=0;i<190;i++){

  particles.push(
    new Particle()
  );
}

/* =======================================================
   CONNECT LINES
======================================================= */

function connect(time){

  const isLight =
  document.body.classList.contains('light');

  for(let a=0;a<particles.length;a++){

    for(let b=a;b<particles.length;b++){

      let dx =
      particles[a].x - particles[b].x;

      let dy =
      particles[a].y - particles[b].y;

      let dist = dx*dx + dy*dy;

      if(dist < 14000){

        const opacity =
        Math.max(
          (
            (1 - dist/14000)
            *
            (
              0.65 +
              Math.sin(
                time * 0.001 + dist
              ) * 0.2
            )
          ),
          0.08
        );

        const gradient =
        ctx.createLinearGradient(
          particles[a].x,
          particles[a].y,
          particles[b].x,
          particles[b].y
        );

        /* DARK MODE */

        if(!isLight){

          gradient.addColorStop(
            0,
            `rgba(140,120,255,${opacity})`
          );

          gradient.addColorStop(
            0.5,
            `rgba(180,90,255,${opacity})`
          );

          gradient.addColorStop(
            1,
            `rgba(90,180,255,${opacity})`
          );

        }else{

          /* LIGHT MODE */

          gradient.addColorStop(
            0,
            `rgba(120,120,255,${opacity})`
          );

          gradient.addColorStop(
            0.5,
            `rgba(160,120,255,${opacity})`
          );

          gradient.addColorStop(
            1,
            `rgba(90,150,255,${opacity})`
          );
        }

        ctx.beginPath();

        ctx.strokeStyle = gradient;

        ctx.lineWidth = 1.2;

        ctx.moveTo(
          particles[a].x,
          particles[a].y
        );

        ctx.lineTo(
          particles[b].x,
          particles[b].y
        );

        ctx.stroke();
      }
    }
  }
}

/* =======================================================
   ANIMATE
======================================================= */

function animate(time){

  ctx.clearRect(0,0,w,h);

  particles.forEach(p=>{
    p.update(time);
  });

  connect(time);

  requestAnimationFrame(animate);
}

animate(0);

/* =======================================================
   TASK CHECK
======================================================= */

document
.querySelectorAll('.task')
.forEach(task=>{

  task.addEventListener('click',()=>{

    task.classList.toggle('done');

  });

});
