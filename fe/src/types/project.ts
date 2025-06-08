export interface Project {
  id: string;
  name: string;
  children?: Project[];
}