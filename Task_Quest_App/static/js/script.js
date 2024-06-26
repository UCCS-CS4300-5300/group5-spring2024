window.addEventListener('load', function(){
  // canvas setup
  const canvas = document.getElementById('canvas1');
  const ctx = canvas.getContext('2d');
  canvas.width = 540;
  canvas.height = 540;

  // game functions
  class InputHandler {  // class for handling input
    constructor(game){
      this.game = game;
      window.addEventListener('keydown', e => {  //If an arrow key or wasd is pressed
        if ((   (e.key === 'ArrowUp') || (e.key === 'w') ||
                (e.key === 'ArrowDown') || (e.key === 's') ||
                (e.key === 'ArrowLeft') || (e.key === 'a') ||
                (e.key === 'ArrowRight') || (e.key === 'd')
             ) && this.game.keys.indexOf(e.key) === -1){  // for the first time
          this.game.keys.push(e.key);
        } 
        else if (e.key === ' '){
          this.game.player.shootTop();
        }
      });
      window.addEventListener('keyup', e => {
        if (this.game.keys.indexOf(e.key) > -1){  //If an arrow key is released
          this.game.keys.splice(this.game.keys.indexOf(e.key), 1);
        }
      });
    }
  }
  class Projectile {  // class to create and handle projectiles
    constructor(game, x, y){
      this.game = game; 
      this.x = x + this.game.player.width * 0.5;
      this.y = y;
      this.width = 5;
      this.height = 15;
      this.speed = 8;
      this.markedForDeletion = false;
    }
    //Continuously updates the Projectile's position and properties
    update(){
      this.y -= this.speed;
      if (this.y < this.game.height * 0.1) this.markedForDeletion = true;
    }
    //Display the Projectile
    draw(context){
      context.fillStyle = 'lime';
      context.fillRect((this.x), this.y, this.width, this.height)
    }
  }
  class Particle {  // class to create and handle particles
    
  }
  class Player {  // class to create and handle player
    constructor(game){
      this.game = game;  //player variables 
      this.width = 52;
      this.height = 68;
      this.x = 250;  
      this.y = 400;
      this.speedY = 0;
      this.speedX = 0;
      this.maxSpeed = parseInt(document.getElementById('player-speed').value);
      this.projectiles = [];
      this.damage = parseInt(document.getElementById('player-damage').value)
      this.image = document.getElementById('Player');
    }

    update(){
      if ((this.game.keys.includes('ArrowUp') || this.game.keys.includes('w')) && this.y > 0) this.speedY = -this.maxSpeed * 1.5;
      else if ((this.game.keys.includes('ArrowDown') || this.game.keys.includes('s')) && this.y + this.height < this.game.height) this.speedY = this.maxSpeed * 1.5;
      else this.speedY = 0;

      if ((this.game.keys.includes('ArrowLeft') || this.game.keys.includes('a')) && this.x > 0) this.speedX = -this.maxSpeed;
      else if ((this.game.keys.includes('ArrowRight') || this.game.keys.includes('d')) && this.x + this.width < this.game.width) this.speedX = this.maxSpeed;
      else this.speedX = 0;

      this.y += this.speedY;
      this.x += this.speedX;

      //Handle Projectiles
      this.projectiles.forEach(projectile => {
        projectile.update();
      });
      this.projectiles = this.projectiles.filter(projectile => !projectile.markedForDeletion);
    }

    draw(context){
      //context.fillStyle = 'grey';
      //context.fillRect(this.x, this.y, this.width, this.height);
      context.drawImage(this.image, this.x, this.y);
      this.projectiles.forEach(projectile => {
        projectile.draw(context);
      });
    }
    //Create a new Projectile
    shootTop(){
      if(this.game.ammo > 0){
        this.projectiles.push(new Projectile(this.game, this.x, this.y));
        this.game.ammo--;
      }
    }

    refillAmmo(){
      this.game.ammo = this.game.maxAmmo;
    }

    clearEnemies(){
      this.game.enemies = [];
    }
  }
  
  class Enemy {    //Class to create and handle enemies
    constructor(game){
      this.game = game;        //Enemy variables
      this.y = 0;
      this.speedY = Math.random() * 1.5 + 0.5;
      this.markedForDeletion = false;
      this.lives = parseInt(document.getElementById('enemy-health').value) + this.game.difficulty;
      this.score = this.lives;
      this.bonusTime = 1;
    }

    update(){
      this.y += this.speedY;
      if (this.y + this.height > this.game.height){
        this.markedForDeletion = true;
        if (!this.game.gameOver) this.game.timeLimit -= this.bonusTime * 1000;
      }
    }

    draw(context){
      //context.fillStyle = 'red';
      //context.fillRect(this.x, this.y, this.width, this.height);
      context.drawImage(this.image, this.x, this.y);
      //context.fillStyle = 'black';
      //context.font = '20px Arial';
      //context.fillText(this.lives, this.x, this.y);
    }
  }
  //Subclasses of Enemy
  class Fighter extends Enemy {
    constructor(game){
      super(game);
      this.width = 87;
      this.height = 102;
      this.x = Math.random() * (this.game.width * 0.9 - this.width);
      this.type = 'fighter';

      this.image = document.getElementById('Fighter');
    }
  }

  class Clearer extends Enemy{
    constructor(game){
      super(game);
      this.width = 26;
      this.height = 26;
      this.lives = 1;
      this.x = Math.random() * (this.game.width * 0.9 - this.width);
      this.speedY = 6;
      this.bonusTime = 0;
      this.score = 0;
      this.type = 'clear';

      this.image = document.getElementById('Clear');
    }
  }

    class Refiller extends Enemy{
      constructor(game){
        super(game);
        this.width = 28;
        this.height = 36;
        this.lives = 1;
        this.x = Math.random() * (this.game.width * 0.9 - this.width);
        this.speedY = 4;
        this.bonusTime = 0;
        this.score = 0;
        this.type = 'refill';

        this.image = document.getElementById('Refill');
      }
  }
  
//Class to create and handle image layers  
  class Layer {
    constructor(game, image, speedModifier){
      this.game = game;
      this.image = image;
      this.speedModifier = speedModifier;
      this.width = 540;
      this.height = 960;
      this.x = 0;
      this.y = 0;
    }

    update(){
      if (this.y >= this.height) this.y = 0;
      this.y += this.game.speed * this.speedModifier;
    }

    draw(context){
      context.drawImage(this.image, this.x, this.y);
      context.drawImage(this.image, this.x, this.y - this.height);
    }
  }

  //Class to create and handle the background
  class Background {
    constructor(game){
      this.game = game;
      this.image1 = document.getElementById('layer1');
      this.layer1 = new Layer(this.game, this.image1, 1);
      this.layers = [this.layer1];
    }

    update(){
      this.layers.forEach(layer => layer.update());
    }

    draw(context){
      this.layers.forEach(layer => layer.draw(context));
    }
  }

  //Class to create and handle the User Interface
  class UI {
    constructor(game){
      this.game = game;
      this.fontSize = 25;
      this.fontFamily = 'Helvetica';
      this.color = 'lime';
    }
    draw(context){      
      context.save();
      //Ammo Counter
      context.fillStyle = this.color;
      for (let i = 0; i < this.game.ammo; i++){
        context.fillRect(20 + 5 * i, 10, 3, 20);
      }

      //Timer
      const formattedTime = (this.game.gameTime * 0.001).toFixed(1);
      const timeLeft = ((this.game.timeLimit * 0.001) - formattedTime).toFixed(1);
      context.fillText('Timer: ' + timeLeft, 20, 50);

      
      //Game Over Message
      if (this.game.gameOver){
        context.textAlign = 'center';
        let message1;
        let message2;
        if (this.game.score > this.game.winningScore){
          message1 = "You Win!";
          message2 = "Well Done!";
        } else {
          message1 = "You Lose!";
          message2 = "Try Again!";
        }
        context.font = '50px ' + this.fontFamily;
        context.fillText(message1, this.game.width * 0.5, this.game.height * 0.5 - 40);
        context.font = '25px ' + this.fontFamily;
        context.fillText(message2, this.game.width * 0.5, this.game.height * 0.5 + 40);

        document.formName.inputName.value=formattedTime;

      }
      context.restore();
    }
  }

  //Main Class to create and control all elements of a game
  class Game {
    constructor(width, height){      //Game variables
      this.width = width;
      this.height = height;
      this.background = new Background(this);
      this.player = new Player(this);
      this.input = new InputHandler(this);
      this.ui = new UI(this);
      this.keys = [];
      this.enemies = [];
      this.enemyTimer = 0;
      this.enemyInterval = 1000;
      this.ammo = 20;
      this.maxAmmo = 50;
      this.ammoTimer = 0;
      this.ammoInterval = parseInt(document.getElementById('player-recharge').value);
      this.score = 0;
      this.gameOver = false;
      this.score = 0;
      this.winningScore = parseInt(document.getElementById('target-score').value);
      this.gameTime = 0;
      this.timeLimit = parseInt(document.getElementById('starting-time').value);
      this.speed = 1;
      this.difficultyTimer = 20000;
      this.difficulty = 0;
    }
    
    update(deltaTime){
      //Tracks time since game started
      if (!this.gameOver) this.gameTime += deltaTime;

      //Increases difficulty as game progresses
      if (Math.floor(this.gameTime % this.difficultyTimer) < 20) this.difficulty++;
      
      //Ends the game when time runs out
      if (this.gameTime > this.timeLimit) this.gameOver = true;

      this.background.update();
      this.player.update();

      //Regenerates ammo
      if (this.ammoTimer > this.ammoInterval){
        if (this.ammo < this.maxAmmo){
          this.ammo++;
        }
        this.ammoTimer = 0;
      } else {
        this.ammoTimer += deltaTime;
      }

      //Handles enemy collisions with player
      this.enemies.forEach(enemy => {
        enemy.update();
        if (this.checkCollision(this.player, enemy)){
          enemy.markedForDeletion = true;
          if (enemy.type === 'refill') this.player.refillAmmo();
          else if (enemy.type === 'clear') this.player.clearEnemies();
          if (!this.gameOver) this.timeLimit -= enemy.bonusTime * 1000;
        }

        //Handles enemy collisions with projectiles
        this.player.projectiles.forEach(projectile => {
          if (this.checkCollision(projectile, enemy)) {
            enemy.lives -= this.player.damage;
            projectile.markedForDeletion = true;
            if (enemy.lives <= 0){
              enemy.markedForDeletion = true;
              if (!this.gameOver){
                this.score += enemy.score;
                this.timeLimit += enemy.bonusTime * 1000;
              }
              //if (this.score > this.winningScore) this.gameOver = true;
            }
          }
        });
      });
      //Deletes enemies that are marked for deletion
      this.enemies = this.enemies.filter(enemy => !enemy.markedForDeletion);

      //Spawns enemies when the game is not over
      if (this.enemyTimer > this.enemyInterval && !this.gameOver){
        this.addEnemy();
        this.enemyTimer = 0;
      } else {
        this.enemyTimer += deltaTime;
      }
    }

    //Draws all the game elements
    draw(context){
      this.background.draw(context);
      
      this.player.draw(context);
      
      this.ui.draw(context);

      this.enemies.forEach(enemy => {
        enemy.draw(context);
      });
    }

    //Method to create a new enemy
    addEnemy(){

      const random = Math.floor(Math.random() * (26 - 1) + 1);
      
      if (random == 25){
        this.enemies.push(new Refiller(this));
      }
      else if (random == 1){
        this.enemies.push(new Clearer(this));
      }
      else{
        this.enemies.push(new Fighter(this));
      }
    }

    //Method to check for collision between two objects
    checkCollision(rect1, rect2){
      return (rect1.x < rect2.x + rect2.width &&
              rect1.x + rect1.width > rect2.x &&
              rect1.y < rect2.y + rect2.height &&
              rect1.height + rect1.y > rect2.y);
    }
  }

  //Creates a game object
  const game = new Game(canvas.width, canvas.height);

  //Variable to track time
  let lastTime = 0;

  //Method that Updates the game and draws it
  function animate(timeStamp){
    const deltaTime = timeStamp - lastTime;
    lastTime = timeStamp;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    game.update(deltaTime);
    game.draw(ctx);
    requestAnimationFrame(animate);
  }

  //Update and draw the game
  animate(0);
});